import { createClient } from '@libsql/client'
import path from 'path'

// Client is created once and reused
const url = process.env.TURSO_DATABASE_URL || `file:${path.join(process.cwd(), '../fleet_pro/fleet_pro.db')}`
const authToken = process.env.TURSO_AUTH_TOKEN

const client = createClient({
  url: url,
  authToken: authToken,
})

export async function getDb() {
  // Return an object that mimics the sqlite-style methods used in the app
  return {
    all: async (sql: string, args: any[] = []) => {
      const rs = await client.execute({ sql, args })
      // LibSQL rows are objects, so we can return them as-is
      return rs.rows
    },
    get: async (sql: string, args: any[] = []) => {
      const rs = await client.execute({ sql, args })
      return rs.rows[0]
    },
    run: async (sql: string, args: any[] = []) => {
      const rs = await client.execute({ sql, args })
      return { lastID: rs.lastInsertRowid }
    }
  }
}