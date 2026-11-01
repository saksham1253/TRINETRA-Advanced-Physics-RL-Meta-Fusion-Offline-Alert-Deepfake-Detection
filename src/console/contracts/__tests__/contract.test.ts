// Contract test: every message of the recorded gateway session (tools/mock_gateway.py --record) validates against the schema.
import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { validateLiveEvent } from '../liveEvent'

describe('live event contract', () => {
  it('recorded replay session validates', () => {
    const lines = readFileSync('public/replay/session_demo.jsonl', 'utf8').split('\n').filter(Boolean)
    expect(lines.length).toBeGreaterThan(100)
    for (const l of lines) expect(validateLiveEvent(JSON.parse(l))).toEqual([])
  })
  it('rejects an event without the human approval gate', () => {
    const e = JSON.parse(readFileSync('public/replay/session_demo.jsonl', 'utf8').split('\n')[0])
    e.decision.requires_approval = false
    expect(validateLiveEvent(e)).toContain('requires_approval must be true (Rule 19)')
  })
})
