import { getDb } from './lib/db';

async function test() {
  const db = await getDb();
  try {
    const res = await db.get(`SELECT COUNT(*) as c FROM cars`);
    console.log("SUCCESS:", res);
  } catch (err: any) {
    console.error("FAILURE:", err.message);
  }
}

test();
