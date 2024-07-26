import React, { useCallback } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from '@xyflow/react';
 
import '@xyflow/react/dist/style.css';

//MongoDB
const mongoose = require('mongoose');
const uri = "...";

const clientOptions = { serverApi: { version: '1', strict: true, deprecationErrors: true } };

//React Flow workflows
const initialNodes = [
  { id: '1', position: { x: 0, y: 0 }, data: { label: '1' } },
  { id: '2', position: { x: 0, y: 100 }, data: { label: '2' } },
];
const initialEdges = [{ id: 'e1-2', source: '1', target: '2' }];



export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
 
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  const exportToJson = async () => {
    const workflow = { "nodes": nodes, "edges": edges }
    //const workflow = [nodes, edges]
    const workflowJSON = JSON.stringify(workflow);
    console.log(workflowJSON);

    const url = 'https://localhost/api';
    const [response, setResponse] = useState(null);

    //console.log(workflow);
    // You can also save this JSON to MongoDB
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: workflowJSON,
      });
      const jsonResponse = await response.json();
      setResponse(jsonResponse);
    } catch (error) {
      console.error('Error:', error);
    }

  };
 
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      >
        <Controls />
        <MiniMap />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
      <button onClick={exportToJson}>Export to JSON</button>
    </div>
  );
}