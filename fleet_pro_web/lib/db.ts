import { createClient } from '@libsql/client'
import path from 'path'

// Get credentials from environment
const url = process.env.TURSO_DATABASE_URL
const authToken = process.env.TURSO_AUTH_TOKEN

// Fallback to local file for dev, but in production we MUST have a URL
const clientUrl = url || `file:${path.join(process.cwd(), '../fleet_pro/fleet_pro.db')}`

const client = createClient({
  url: clientUrl,
  authToken: authToken,
})

// Log connection status in production for debugging (without leaking the secret)
if (process.env.NODE_ENV === 'production' && !url) {
  console.error("⚠️ DATA ERROR: TURSO_DATABASE_URL is missing in environment variables!")
}

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
  return {
    all: async (sql: string, args: any[] = []) => {
      try {
        const rs = await client.execute({ sql, args })
        return rs.rows.map(r => convertNumbers(r))
      } catch (err: any) {
        if (err.message?.includes('status 400')) {
          console.error(`❌ DB ALL Error (Status 400): Is the schema initialized on Turso? Try visiting /api/migrate`)
        } else {
          console.error(`❌ DB ALL Error [${sql}]:`, err.message)
        }
        throw err
      }
    },
    get: async (sql: string, args: any[] = []) => {
      try {
        const rs = await client.execute({ sql, args })
        return rs.rows[0] ? convertNumbers(rs.rows[0]) : null
      } catch (err: any) {
        if (err.message?.includes('status 400')) {
          console.error(`❌ DB GET Error (Status 400): Is the schema initialized on Turso? Try visiting /api/migrate`)
        } else {
          console.error(`❌ DB GET Error [${sql}]:`, err.message)
        }
        throw err
      }
    },
    run: async (sql: string, args: any[] = []) => {
      try {
        const rs = await client.execute({ sql, args })
        return { lastID: convertNumbers(rs.lastInsertRowid) }
      } catch (err: any) {
        console.error(`❌ DB RUN Error [${sql}]:`, err.message)
        throw err
      }
    }
  }
}