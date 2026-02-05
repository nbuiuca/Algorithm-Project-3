# pip install networkx matplotlib
import networkx as nx
import matplotlib.pyplot as plt

# ---------- Original digraph (exactly as in the picture) ----------
edges = [
    (4, 1), (4, 2), (4, 12),
    (2, 1),
    (1, 3),
    (3, 2), (3, 5),
    (12, 11),
    (10, 11),
    (9, 11), (10, 9),
    (9, 5),
    (5, 8), (5, 6),
    (6, 8), (6, 7), (7, 10),
    (8, 9), (8, 10),
    (6, 10),
]

G = nx.DiGraph()
G.add_edges_from(edges)

print(f"Nodes: {sorted(G.nodes())}")
print(f"Edges ({G.number_of_edges()}): {sorted(G.edges())}")

# ---------- (a) Strongly connected components ----------
sccs = list(nx.strongly_connected_components(G))
sccs_sorted = sorted([sorted(S) for S in sccs], key=lambda S: S[0])
print("\nStrongly connected components (SCCs):")
for i, comp in enumerate(sccs_sorted, 1):
    print(f"  C{i}: {comp}")

# ---------- DRAW: Original digraph ----------
# Hand-tuned positions to resemble the assignment picture
pos = {
    4:(0.0,0.3), 1:(0.6,0.35), 2:(0.55,0.15), 3:(0.9,0.30),
    12:(0.4,-0.15), 11:(1.1,-0.35),
    9:(1.15,-0.05), 5:(1.00,0.10), 8:(1.35,-0.05),
    6:(1.15,-0.35), 10:(1.35,-0.35), 7:(1.35,-0.55),
}
plt.figure(figsize=(9,6))
nx.draw_networkx(
    G, pos,
    with_labels=True, node_size=900, arrowsize=20, font_weight="bold"
)
plt.title("Original Directed Graph (Digraph)")
plt.axis("off")
plt.tight_layout()
plt.savefig("original_digraph.png", dpi=200)
plt.show()

# ---------- (b) Meta graph (condensation DAG) ----------
C = nx.condensation(G)  # DAG of SCCs; nodes are 0..k-1 with 'members' attribute
id_to_members = {i: sorted(data['members']) for i, data in C.nodes(data=True)}

print("\nMeta-graph nodes (component_id -> members):")
for cid in sorted(id_to_members):
    print(f"  {cid}: {id_to_members[cid]}")

print("\nMeta-graph edges (between components):")
for u, v in sorted(C.edges()):
    print(f"  {id_to_members[u]}  ->  {id_to_members[v]}")

# Labels like "{1,2,3}" etc.
meta_labels = {
    cid: "{" + ",".join(map(str, id_to_members[cid])) + "}"
    for cid in C.nodes()
}

# ---------- DRAW: Meta/SCC graph ----------
plt.figure(figsize=(8,5))
# layout for DAG; spring_layout is fine, or use shell_layout for simple chains
pos_meta = nx.spring_layout(C, seed=7)
nx.draw_networkx(C, pos_meta, with_labels=False, node_size=1100, arrowsize=20)
nx.draw_networkx_labels(C, pos_meta, labels=meta_labels, font_weight="bold")
plt.title("Meta Graph (SCC Condensation DAG)")
plt.axis("off")
plt.tight_layout()
plt.savefig("meta_graph_scc.png", dpi=200)
plt.show()

# ---------- (c) Topological order ----------
topo = list(nx.topological_sort(C))
topo_components = [id_to_members[cid] for cid in topo]
print("\nOne valid topological order of SCCs:")
print("  " + "  ->  ".join("{" + ",".join(map(str, comp)) + "}" for comp in topo_components))