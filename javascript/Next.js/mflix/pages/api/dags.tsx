import clientPromise from "../../lib/mongodb";
import { NextApiRequest, NextApiResponse } from 'next';

export default async (req: NextApiRequest, res: NextApiResponse) => {
    try {
        const client = await clientPromise;
        const db = client.db("dagdb");
        const dags = await db
            .collection("dags")
            .find({})
            //.sort({ metacritic: -1 })
            .limit(10)
            .toArray();
        res.json(dags);
    } catch (e) {
        console.error(e);
    }
}
