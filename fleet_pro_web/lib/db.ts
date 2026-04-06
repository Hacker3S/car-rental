import { createClient } from '@libsql/client'
import path from 'path'

// Client is created once and reused
const url = process.env.TURSO_DATABASE_URL || `file:${path.join(process.cwd(), '../fleet_pro/fleet_pro.db')}`
const authToken = process.env.TURSO_AUTH_TOKEN

const client = createClient({
  url: url,
  authToken: authToken,
})

// Helper to convert LibSQL BigInts to numbers for JSON/TS compatibility
function convertNumbers(obj: any): any {
  if (obj === null || typeof obj !== 'object') {
    return typeof obj === 'bigint' ? Number(obj) : obj
  }
  if (Array.isArray(obj)) {
    return obj.map(convertNumbers)
  }
  const newObj: any = {}
  for (const [key, val] of Object.entries(obj)) {
    newObj[key] = convertNumbers(val)
  }
  return newObj
}

export async function getDb() {
  // Return an object that mimics the sqlite-style methods used in the app
  return {
    all: async (sql: string, args: any[] = []) => {
      const rs = await client.execute({ sql, args })
      return rs.rows.map(r => convertNumbers(r))
    },
    get: async (sql: string, args: any[] = []) => {
      const rs = await client.execute({ sql, args })
      return rs.rows[0] ? convertNumbers(rs.rows[0]) : null
    },
    run: async (sql: string, args: any[] = []) => {
      const rs = await client.execute({ sql, args })
      return { lastID: convertNumbers(rs.lastInsertRowid) }
    }
  }
}