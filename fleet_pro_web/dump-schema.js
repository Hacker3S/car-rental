import sqlite3 from 'sqlite3';
import path from 'path';

const dbPath = path.join(process.cwd(), '../fleet_pro/fleet_pro.db');
const db = new sqlite3.Database(dbPath);

db.serialize(() => {
  db.all("SELECT name, sql FROM sqlite_master WHERE type='table'", (err, rows) => {
    if (err) {
      console.error(err);
    } else {
      rows.forEach(row => {
        console.log(`-- TABLE: ${row.name}\n${row.sql};\n`);
      });
    }
    db.close();
  });
});
