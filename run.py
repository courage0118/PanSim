from 1ScenarioSetup import Scenario
from 2
from 3


scenario_config = SecenarioConfig()
IDMSecenario = Scenario(config)

model_params = IDMParams()
state = step(model_params)

observer(state)