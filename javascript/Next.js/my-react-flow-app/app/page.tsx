import { useState } from 'react';
import ReactFlow, { addEdge, MiniMap, Controls, Background } from 'reactflow';
import 'reactflow/dist/style.css';

const initialElements = [
  { id: '1', type: 'input', data: { label: 'Start' }, position: { x: 250, y: 5 } },
  { id: '2', data: { label: 'Task' }, position: { x: 100, y: 100 } },
  { id: '3', data: { label: 'End' }, position: { x: 400, y: 100 } },
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e2-3', source: '2', target: '3', animated: true }
];

function Flow() {
  const [elements, setElements] = useState(initialElements);

  const saveWorkflow = async () => {
    const response = await fetch('/api/save-workflow', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(elements)
    });

    const result = await response.json();
    if (result.success) {
      alert(`Workflow saved with ID: ${result.id}`);
    } else {
      alert(`Error saving workflow: ${result.error}`);
    }
  };

  return (
    <div style={{ height: 600 }}>
      <ReactFlow
        elements={elements}
        onElementsRemove={(elementsToRemove) => setElements((els) => removeElements(elementsToRemove, els))}
        onConnect={(params) => setElements((els) => addEdge(params, els))}
        onLoad={(reactFlowInstance) => reactFlowInstance.fitView()}
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
      <button onClick={saveWorkflow}>Save Workflow</button>
    </div>
  );
}

export default Flow;
