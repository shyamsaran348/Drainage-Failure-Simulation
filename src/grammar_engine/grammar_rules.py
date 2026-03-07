import networkx as nx

class GrammarRule:
    """
    Base class for Graph Grammar rules.
    LHS -> RHS
    """
    def __init__(self, name):
        self.name = name

    def condition(self, graph, element):
        """
        LHS check. Returns True if the rule should be applied.
        'element' is either a node ID or an edge tuple (u, v).
        """
        raise NotImplementedError

    def apply(self, graph, element):
        """
        RHS transformation.
        """
        raise NotImplementedError

class OverloadRule(GrammarRule):
    """
    Rule 3: Pipe Overload
    Condition: flow > capacity
    Transformation: status = 'overloaded'
    """
    def __init__(self):
        super().__init__("OverloadRule")

    def condition(self, graph, edge):
        u, v = edge
        attr = graph.edges[u, v]
        # Calculate dynamic capacity if not stored
        return attr['status'] == 'active' and attr['flow'] > attr['capacity']

    def apply(self, graph, edge):
        u, v = edge
        graph.edges[u, v]['status'] = 'overloaded'
        if 'overload_duration' not in graph.edges[u, v]:
            graph.edges[u, v]['overload_duration'] = 0
            
class BlockageFormationRule(GrammarRule):
    """
    Rule 4: Blockage Formation
    Condition: overloaded for > threshold steps
    Transformation: status = 'blocked'
    """
    def __init__(self, threshold=3):
        super().__init__("BlockageFormationRule")
        self.threshold = threshold

    def condition(self, graph, edge):
        u, v = edge
        attr = graph.edges[u, v]
        return attr['status'] == 'overloaded' and attr.get('overload_duration', 0) >= self.threshold

    def apply(self, graph, edge):
        u, v = edge
        graph.edges[u, v]['status'] = 'blocked'
        print(f"[RULE] {self.name}: Pipe ({u}->{v}) is now BLOCKED due to sustained overload.")

class CascadingFailureRule(GrammarRule):
    """
    Rule 7: Cascading Failure
    Condition: Blocked downstream pipe causes upstream pressure increase.
    Transformation: Mark upstream node for pressure risk.
    """
    def __init__(self):
        super().__init__("CascadingFailureRule")

    def condition(self, graph, edge):
        u, v = edge
        # If edge is blocked, check its UPSTREAM edges
        return graph.edges[u, v]['status'] == 'blocked'

    def apply(self, graph, edge):
        u, v = edge
        # Propagate pressure to all edges entering u
        for pred in graph.predecessors(u):
            if graph.edges[pred, u]['status'] == 'active':
                graph.edges[pred, u]['pressure_risk'] = True
                # Potentially decrease capacity or increase blockage chance
                graph.edges[pred, u]['capacity'] *= 0.8 

class OverflowRule(GrammarRule):
    """
    Rule 6: Node Overflow
    Condition: water_level > capacity
    Transformation: type = 'flood'
    """
    def __init__(self):
        super().__init__("OverflowRule")

    def condition(self, graph, node):
        attr = graph.nodes[node]
        return attr['type'] != 'flood' and attr['water_level'] > attr['capacity']

    def apply(self, graph, node):
        graph.nodes[node]['type'] = 'flood'
        print(f"[RULE] {self.name}: Node {node} is FLOODING.")

class FlowReroutingRule(GrammarRule):
    """
    Rule 5: Flow Rerouting
    Condition: Path blocked, alternate path exists.
    """
    def __init__(self):
        super().__init__("FlowReroutingRule")

    def condition(self, graph, node):
        blocked_out = [v for _, v, a in graph.out_edges(node, data=True) if a['status'] == 'blocked']
        if not blocked_out: return False
        
        active_paths = [v for _, v, a in graph.out_edges(node, data=True) if a['status'] == 'active']
        return len(active_paths) > 0

    def apply(self, graph, node):
        graph.nodes[node]['reroute_active'] = True
        print(f"[RULE] {self.name}: Node {node} is rerouting flow.")
