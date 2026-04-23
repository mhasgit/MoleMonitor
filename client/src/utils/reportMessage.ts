/**
 * Build report message from decision + metrics so "In simple terms" always matches the Checks (triggered_rules).
 * Use this instead of raw message_text so content is consistent with Color/Size/Shape status.
 */
const DISCLAIMER = 'This tool does not provide medical diagnosis. If you are concerned, seek professional advice.'

type Decision = {
  summary_reason?: string
  triggered_rules?: string[]
}

export function buildReportSummary(decision: Decision | null | undefined): string {
  return (decision?.summary_reason ?? 'No summary available.').trim()
}

export function buildSimpleTerms(
  decision: Decision | null | undefined,
  metrics: Record<string, unknown> | null | undefined
): { size: string; color: string; shape: string } {
  const triggered = new Set((decision?.triggered_rules ?? []) as string[])

  const sizeTriggered = triggered.has('area_change_percent') || triggered.has('diameter_increase_mm')
  const scaleAvailable = metrics?.scale_available === true
  const diamMm = metrics?.diam_change_mm as number | undefined
  const areaCh = (metrics?.area_change_percent as number) ?? 0

  let size = 'about the same.'
  if (sizeTriggered) {
    if (scaleAvailable && diamMm != null) {
      size = diamMm > 0
        ? 'the newer image shows a slightly larger area than the older one.'
        : 'the newer image shows a slightly smaller area than the older one.'
    } else {
      size = areaCh > 0
        ? 'the newer image shows a larger area than the older one. (Scale not available for exact measurements.)'
        : 'the newer image shows a smaller area than the older one. (Scale not available for exact measurements.)'
    }
  }

  let color = 'no notable change.'
  if (triggered.has('color_deltaE')) {
    const deltaE = (metrics?.color_deltaE as number) ?? 0
    color = deltaE >= 6
      ? 'a noticeable color difference between the two images.'
      : 'a slight color difference between the two images.'
  }

  const shape = triggered.has('irregularity_delta')
    ? 'the outline appears somewhat different between the two images.'
    : 'similar in both images.'

  return { size, color, shape }
}

export function buildReportMessage(
  decision: Decision | null | undefined,
  metrics: Record<string, unknown> | null | undefined
): string {
  const summary = buildReportSummary(decision)
  const simpleTerms = buildSimpleTerms(decision, metrics)
  const parts: string[] = [summary, '', 'In simple terms:']

  parts.push(`• Size: ${simpleTerms.size}`)
  parts.push(`• Color: ${simpleTerms.color}`)
  parts.push(`• Shape: ${simpleTerms.shape}`)

  parts.push('', DISCLAIMER)
  return parts.join('\n')
}

export function extractSimpleTermsFromMessage(
  messageText: string | null | undefined
): { size: string; color: string; shape: string } | null {
  if (!messageText) return null
  const lines = messageText
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
  const sizeLine = lines.find((line) => line.startsWith('• Size:'))
  const colorLine = lines.find((line) => line.startsWith('• Color:'))
  const shapeLine = lines.find((line) => line.startsWith('• Shape:'))
  if (!sizeLine && !colorLine && !shapeLine) return null
  return {
    size: sizeLine ? sizeLine.replace(/^• Size:\s*/, '') : 'about the same.',
    color: colorLine ? colorLine.replace(/^• Color:\s*/, '') : 'no notable change.',
    shape: shapeLine ? shapeLine.replace(/^• Shape:\s*/, '') : 'similar in both images.',
  }
}
