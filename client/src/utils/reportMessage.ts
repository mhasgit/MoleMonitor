/**
 * Build report message from decision + metrics so "In simple terms" always matches the Checks (triggered_rules).
 * Use this instead of raw message_text so content is consistent with Color/Size/Shape status.
 */
const DISCLAIMER = 'This tool does not provide medical diagnosis. If you are concerned, seek professional advice.'

type Decision = {
  summary_reason?: string
  triggered_rules?: string[]
}

export function buildReportMessage(
  decision: Decision | null | undefined,
  metrics: Record<string, unknown> | null | undefined
): string {
  const triggered = new Set((decision?.triggered_rules ?? []) as string[])
  const summary = (decision?.summary_reason ?? 'No summary available.').trim()
  const parts: string[] = [summary, '', 'In simple terms:']

  const sizeTriggered = triggered.has('area_change_percent') || triggered.has('diameter_increase_mm')
  const scaleAvailable = metrics?.scale_available === true
  const diamMm = metrics?.diam_change_mm as number | undefined
  const areaCh = (metrics?.area_change_percent as number) ?? 0

  if (sizeTriggered) {
    if (scaleAvailable && diamMm != null) {
      if (diamMm > 0) {
        parts.push('• Size: the newer image shows a slightly larger area than the older one.')
      } else {
        parts.push('• Size: the newer image shows a slightly smaller area than the older one.')
      }
    } else {
      if (areaCh > 0) {
        parts.push('• Size: the newer image shows a larger area than the older one. (Scale not available for exact measurements.)')
      } else {
        parts.push('• Size: the newer image shows a smaller area than the older one. (Scale not available for exact measurements.)')
      }
    }
  } else {
    parts.push('• Size: about the same.')
  }

  if (triggered.has('color_deltaE')) {
    const deltaE = (metrics?.color_deltaE as number) ?? 0
    parts.push(deltaE >= 6 ? '• Color: a noticeable color difference between the two images.' : '• Color: a slight color difference between the two images.')
  } else {
    parts.push('• Color: no notable change.')
  }

  if (triggered.has('irregularity_delta')) {
    parts.push('• Shape: the outline appears somewhat different between the two images.')
  } else {
    parts.push('• Shape: similar in both images.')
  }

  parts.push('', DISCLAIMER)
  return parts.join('\n')
}
