"""P1.6 · Traces OpenTelemetry de bout en bout, visibles dans Phoenix.

Une conversation τ³ donne un arbre :
  conversation <tâche>
  ├── tour agent        → appel LLM (OpenInference : tokens, messages) → requête HTTP → vLLM (ses propres spans)
  ├── outil <nom>       → requête HTTP MCP → serveur : exécution de l'outil
  └── tour client       → appel LLM du client simulé (OpenRouter)

La propagation passe par l'en-tête HTTP standard `traceparent` (W3C), injecté par l'instrumentation httpx :
vers vLLM (qui le lit nativement) et vers le serveur MCP (qui le lit dans `serveur.py`).

Activé si la variable TRACES vaut 1. Phoenix : PHOENIX_URL (défaut http://127.0.0.1:6006).
"""
import atexit
import functools
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.id_generator import IdGenerator
from opentelemetry.sdk.trace.export import BatchSpanProcessor

PROJET = os.environ.get("TRACES_PROJET", "agent-sous-charge")
actif = os.environ.get("TRACES") == "1"


class IdentifiantsSystème(IdGenerator):
    """Identifiants de trace tirés du hasard du système, pas du module `random`.

    τ³ fixe la graine de `random` (--seed) pour rendre les conversations reproductibles ; le générateur
    par défaut d'OpenTelemetry tire ses identifiants de ce même `random`. Chaque essai produisait donc
    les mêmes identifiants que le précédent, et Phoenix rangeait les nouveaux spans dans les anciennes traces.
    """

    def generate_span_id(self) -> int:
        return int.from_bytes(os.urandom(8), "big") or 1

    def generate_trace_id(self) -> int:
        return int.from_bytes(os.urandom(16), "big") or 1


def installer(service: str) -> trace.Tracer:
    """Fournisseur de traces vers Phoenix ; renvoie un traceur (inactif si TRACES != 1)."""
    if actif:
        url = os.environ.get("PHOENIX_URL", "http://127.0.0.1:6006").rstrip("/")
        fournisseur = TracerProvider(id_generator=IdentifiantsSystème(), resource=Resource.create({
            "service.name": service, "openinference.project.name": PROJET}))
        fournisseur.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{url}/v1/traces")))
        trace.set_tracer_provider(fournisseur)
        # Le span « conversation » se ferme en dernier : sans vidage à la sortie, il est perdu.
        atexit.register(fournisseur.shutdown)
    return trace.get_tracer(service)


def _envelopper(cls, methode: str, nom_span, attributs=lambda self, *a, **k: {}):
    origine = getattr(cls, methode)

    @functools.wraps(origine)
    def enveloppe(self, *args, **kwargs):
        with trace.get_tracer("tau3").start_as_current_span(nom_span(self, *args, **kwargs),
                                                             attributes=attributs(self, *args, **kwargs)):
            return origine(self, *args, **kwargs)

    setattr(cls, methode, enveloppe)


def instrumenter_llm() -> None:
    """À appeler AVANT tout import de tau2 : τ³ fait `from litellm import completion`, qu'il faut
    instrumenter avant qu'il n'en garde une référence."""
    if not actif:
        return
    installer("tau3")
    from openinference.instrumentation.litellm import LiteLLMInstrumentor
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

    LiteLLMInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()


def instrumenter_tau3() -> None:
    """Côté τ³ : conversation, tours agent et client (après instrumenter_llm)."""
    if not actif:
        return
    from tau2.agent.llm_agent import LLMAgent
    from tau2.orchestrator.orchestrator import BaseOrchestrator
    from tau2.user.user_simulator import UserSimulator

    _envelopper(BaseOrchestrator, "run", lambda self: f"conversation {self.task.id}",
                lambda self: {"tache": self.task.id, "domaine": self.environment.get_domain_name()})
    _envelopper(LLMAgent, "generate_next_message", lambda self, *a, **k: "tour agent")
    _envelopper(UserSimulator, "generate_next_message", lambda self, *a, **k: "tour client")
