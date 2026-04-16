import yaml
from data_and_dragons.models import Scenario

class ScenarioLoader:
    """Loads a Scenario from a YAML file."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> Scenario:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        # Pydantic handles validation parsing dict into Scenario model
        return Scenario.model_validate(data)
