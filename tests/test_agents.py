import pytest
from agents.experts.financial_agent import FinancialHealthExpert
from agents.experts.utility_agent import UtilityManagementExpert
from agents.experts.vehicle_agent import VehicleManagementExpert

class TestExpertAgents:
    def test_financial_expert_instantiation(self):
        agent = FinancialHealthExpert()
        assert agent.name == "FinancialHealthExpert"
    def test_utility_expert_instantiation(self):
        agent = UtilityManagementExpert()
        assert agent.name == "UtilityManagementExpert"
    def test_vehicle_expert_instantiation(self):
        agent = VehicleManagementExpert()
        assert agent.name == "VehicleManagementExpert"


if __name__ == "__main__":
    pytest.main([__file__]) 