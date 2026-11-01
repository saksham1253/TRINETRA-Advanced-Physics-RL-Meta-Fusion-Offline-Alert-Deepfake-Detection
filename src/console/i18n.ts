// UI strings (i18n keys; no hard-coded labels in components). Hinglish is used only in explanatory text, never in alert labels
// unless chosen. Hindi strings need review by a native speaker before any official showing (FRONTEND/QA.md).
import { useStore, type Lang } from './store'

const S = {
  appTitle: { en: 'TRINETRA Command Console', hi: 'त्रिनेत्र कमांड कंसोल', hinglish: 'TRINETRA Command Console' },
  team: { en: 'Team Sankat Mochak', hi: 'टीम संकट मोचक', hinglish: 'Team Sankat Mochak' },
  prototype: { en: 'Prototype: outputs are not field-validated', hi: 'प्रोटोटाइप: परिणाम क्षेत्र-सत्यापित नहीं हैं', hinglish: 'Prototype: outputs field-validated nahi hain' },
  sim: { en: 'Simulation', hi: 'सिमुलेशन', hinglish: 'Simulation' },
  replay: { en: 'Replay', hi: 'रीप्ले', hinglish: 'Replay' },
  live: { en: 'Live model', hi: 'लाइव मॉडल', hinglish: 'Live model' },
  internet: { en: 'Internet', hi: 'इंटरनेट', hinglish: 'Internet' },
  cellular: { en: 'Cellular', hi: 'मोबाइल नेटवर्क', hinglish: 'Cellular' },
  scenario: { en: 'Scenario', hi: 'परिदृश्य', hinglish: 'Scenario' },
  params: { en: 'Models and parameters', hi: 'मॉडल और पैरामीटर', hinglish: 'Models aur parameters' },
  layers: { en: 'Layers', hi: 'परतें', hinglish: 'Layers' },
  alerts: { en: 'Alerts', hi: 'चेतावनियाँ', hinglish: 'Alerts' },
  evidence: { en: 'Evidence', hi: 'साक्ष्य', hinglish: 'Evidence' },
  lora: { en: 'LoRa mesh', hi: 'LoRa मेश', hinglish: 'LoRa mesh' },
  sitrep: { en: 'Situation', hi: 'स्थिति', hinglish: 'Situation' },
  watch: { en: 'Watch', hi: 'निगरानी', hinglish: 'Watch' },
  warning: { en: 'Warning', hi: 'चेतावनी', hinglish: 'Warning' },
  emergency: { en: 'Emergency', hi: 'आपातकाल', hinglish: 'Emergency' },
  normal: { en: 'Normal', hi: 'सामान्य', hinglish: 'Normal' },
  approve: { en: 'Approve', hi: 'स्वीकृत करें', hinglish: 'Approve' },
  hold: { en: 'Hold', hi: 'रोकें', hinglish: 'Hold' },
  escalate: { en: 'Escalate', hi: 'आगे भेजें', hinglish: 'Escalate' },
  dismiss: { en: 'Dismiss', hi: 'खारिज करें', hinglish: 'Dismiss' },
  demoNoSend: { en: 'Demo: no message is sent to any person or channel', hi: 'डेमो: किसी व्यक्ति या चैनल को संदेश नहीं भेजा जाता', hinglish: 'Demo: kisi ko message nahi bheja jaata' },
  outageBtn: { en: 'Simulate internet and cellular outage', hi: 'इंटरनेट और मोबाइल नेटवर्क विफलता का सिमुलेशन', hinglish: 'Internet aur cellular outage simulate karein' },
  restoreBtn: { en: 'Restore networks', hi: 'नेटवर्क बहाल करें', hinglish: 'Network wapas chalu karein' },
  returnIndia: { en: 'Return to India', hi: 'भारत दृश्य पर लौटें', hinglish: 'India view par wapas' },
  recomputed: { en: 'recomputed in', hi: 'पुनर्गणना', hinglish: 'recompute' },
  onScenario: { en: 'on this simulated scenario', hi: 'इस सिमुलेटेड परिदृश्य पर', hinglish: 'is simulated scenario par' },
  search: { en: 'Place or lat, lon', hi: 'स्थान या lat, lon', hinglish: 'Jagah ya lat, lon' },
}
export type Key = keyof typeof S
export const t = (k: Key, lang: Lang) => S[k][lang] ?? S[k].en
export function useT() {
  const lang = useStore((s) => s.lang)
  return (k: Key) => t(k, lang)
}

export const LEVEL_KEY = ['normal', 'watch', 'warning', 'emergency'] as const
export const ACTION_TEXT: Record<number, { en: string; hinglish: string; hi: string }> = {
  0: { en: 'No action.', hinglish: 'Koi action nahi.', hi: 'कोई कार्रवाई नहीं।' },
  1: { en: 'Verify on camera and keep the area under watch.', hinglish: 'Camera par verify karein aur area par nazar rakhein.', hi: 'कैमरे पर पुष्टि करें और क्षेत्र पर निगरानी रखें।' },
  2: { en: 'Send a field team to verify; prepare local warning.', hinglish: 'Field team bhej kar verify karein; local warning taiyaar rakhein.', hi: 'पुष्टि के लिए क्षेत्रीय दल भेजें; स्थानीय चेतावनी तैयार रखें।' },
  3: { en: 'Escalate to the district authority for an official warning decision.', hinglish: 'Official warning ke faisle ke liye district authority ko escalate karein.', hi: 'आधिकारिक चेतावनी निर्णय हेतु जिला प्राधिकरण को भेजें।' },
}
