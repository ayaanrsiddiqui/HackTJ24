from qiskit import Aer, QuantumCircuit, transpile, assemble
from qiskit.visualization import plot_histogram
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import COBYLA

# Define the problem Hamiltonian
graph = {
    (0, 1): 1,
    (1, 2): 1,
    (2, 3): 1,
    (3, 0): 1
}

# Set up the QuantumCircuit and initialize the QAOA algorithm
n_qubits = len(set(node for edge in graph.keys() for node in edge))  # Determine the number of qubits
p = 1  # Number of QAOA iterations

# Create the QuantumCircuit
qc = QuantumCircuit(n_qubits, n_qubits)

# Apply Hadamard gates to all qubits
qc.h(range(n_qubits))

# Apply the QAOA operators
for edge, weight in graph.items():
    qc.cp(-2 * weight, edge[0], edge[1])
    qc.p(weight, edge[0])
    qc.p(weight, edge[1])

# Measure the qubits
qc.measure(range(n_qubits), range(n_qubits))

# Run the simulation
backend = Aer.get_backend('qasm_simulator')
tqc = transpile(qc, backend)
qaoa_circuit = assemble(tqc)
result = backend.run(qaoa_circuit).result()

# Display the result
counts = result.get_counts()
print("QAOA Result:", counts)
plot_histogram(counts)
