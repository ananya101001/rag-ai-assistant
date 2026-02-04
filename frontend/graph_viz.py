# frontend/graph_viz.py
import streamlit as st
import graphviz

def render_rbac_graph():
    """
    Visualizes the relationship between Roles and Data Classification.
    """
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR') # Left to Right layout

    # 1. Create Role Nodes
    graph.node('J', 'Junior Auditor', shape='ellipse', style='filled', fillcolor='#d1fae5') # Green
    graph.node('M', 'Manager', shape='ellipse', style='filled', fillcolor='#fef08a') # Yellow
    graph.node('A', 'Admin', shape='ellipse', style='filled', fillcolor='#fecaca') # Red

    # 2. Create Data Nodes
    graph.node('Low', '🟢 Public Docs', shape='note')
    graph.node('Med', '🟡 Internal Docs', shape='note')
    graph.node('High', '🔴 Confidential Docs', shape='note')

    # 3. Draw Edges (Who accesses what)
    # Junior
    graph.edge('J', 'Low', color='green')
    
    # Manager
    graph.edge('M', 'Low', color='green')
    graph.edge('M', 'Med', color='orange')
    
    # Admin
    graph.edge('A', 'Low', color='green')
    graph.edge('A', 'Med', color='orange')
    graph.edge('A', 'High', color='red')

    st.graphviz_chart(graph)
    st.caption("Visual representation of the Graph-Based Role Access Control currently active.")