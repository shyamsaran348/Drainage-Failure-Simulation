from src.grammar_engine.grammar_rules import (
    OverloadRule, 
    BlockageFormationRule, 
    CascadingFailureRule, 
    OverflowRule, 
    FlowReroutingRule
)

class RuleEngine:
    """
    Manages and applies a collection of graph grammar rules.
    """
    def __init__(self, use_rerouting=True, use_rules=True):
        self.use_rerouting = use_rerouting
        self.use_rules = use_rules
        self.rules = [
            OverloadRule(),
            BlockageFormationRule(threshold=2), # Sensitive threshold
            OverflowRule(),
            CascadingFailureRule()
        ]
        if use_rerouting:
            self.rules.append(FlowReroutingRule())

    def apply_rules(self, graph):
        if not self.use_rules:
            return []
        
        logs = []
        # Rule nodes/edges are handled dynamically
        from src.grammar_engine.grammar_rules import (OverloadRule, BlockageFormationRule, CascadingFailureRule, OverflowRule, FlowReroutingRule)
        
        for rule in self.rules:
            if isinstance(rule, (OverflowRule, FlowReroutingRule)):
                # Node-based rules
                for node in list(graph.nodes()):
                    if rule.condition(graph, node):
                        rule.apply(graph, node)
                        logs.append(f"Applied {rule.name} to node {node}")
            else:
                # Edge-based rules
                for edge in list(graph.edges()):
                    if rule.condition(graph, edge):
                        rule.apply(graph, edge)
                        logs.append(f"Applied {rule.name} to edge {edge}")
        return logs

if __name__ == "__main__":
    # Test stub
    import networkx as nx
    G = nx.DiGraph()
    G.add_edge(1, 2, flow=5.0, capacity=2.0, status='active')
    G.add_node(1, water_level=15.0, capacity=10.0, status='active', type='junction')
    
    engine = RuleEngine()
    applied = engine.apply_rules(G)
    print(applied)
    print(G.edges[1, 2]['status'])
    print(G.nodes[1]['type'])
