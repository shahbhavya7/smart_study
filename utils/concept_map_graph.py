# concept_map_graph.py

import json
import re
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

def fix_json(raw_json):
    raw_json = re.sub(r'(\d+):\s*{', '{', raw_json)
    raw_json = re.sub(r'}\s*{', '},{', raw_json)
    return raw_json

def plot_concept_map(raw_data):
    cleaned_json = fix_json(raw_data)

    try:
        parsed = json.loads(cleaned_json)
    except json.JSONDecodeError as e:
        st.error(f"JSON parsing error: {e}")
        return

    concepts = parsed.get("concepts", [])
    relationships = parsed.get("relationships", [])

    G = nx.DiGraph()

    # Add nodes with safe access
    for concept in concepts:
        concept_id = concept.get("id")
        label = concept.get("label", "Unknown")
        if concept_id is None:
            st.warning(f"Skipping concept without 'id': {concept}")
            continue
        G.add_node(concept_id, label=label)

    # Add edges with safe access
    for rel in relationships:
        src = rel.get("from")
        tgt = rel.get("to")
        label = rel.get("type", "relates to")
        if src is None or tgt is None:
            st.warning(f"Skipping relationship with missing endpoints: {rel}")
            continue
        G.add_edge(src, tgt, label=label)

    pos = nx.spring_layout(G, k=1.2, iterations=100, seed=42)

    plt.figure(figsize=(20, 14))
    
    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, node_color="#4FC3F7", node_size=2200,
        edgecolors='black', linewidths=2, alpha=0.9
    )
    
    # Draw node labels safely
    labels = {node: G.nodes[node].get('label', str(node)) for node in G.nodes}
    nx.draw_networkx_labels(
        G, pos, labels,
        font_size=12, font_weight="bold", font_family="sans-serif"
    )

    # Draw edges
    nx.draw_networkx_edges(
        G, pos, arrows=True, arrowstyle='->',
        edge_color='#888', width=2, alpha=0.8
    )

    # Draw edge labels
    edge_labels = {(u, v): d.get('label', '') for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels,
        font_size=10, font_color='darkgreen'
    )

    # Final styling
    plt.title("📚 Concept Map", fontsize=18)
    plt.axis('off')
    plt.tight_layout()
    st.pyplot(plt)
