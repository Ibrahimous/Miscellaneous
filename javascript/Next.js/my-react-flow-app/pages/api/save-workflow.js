// pages/api/save-workflow.js
import clientPromise from '../../lib/mongodb';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const client = await clientPromise;
      const db = client.db('your-database-name');
      const collection = db.collection('workflows');
      const workflow = req.body;

      const result = await collection.insertOne(workflow);
      res.status(200).json({ success: true, id: result.insertedId });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
