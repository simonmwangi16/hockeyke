/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string;
  readonly VITE_ADSENSE_CLIENT_ID?: string;
  readonly VITE_ADSENSE_HOME_SLOT?: string;
  readonly VITE_ADSENSE_LEAGUE_SLOT?: string;
  readonly VITE_ADSENSE_TEAM_SLOT?: string;
  readonly VITE_ADSENSE_FOOTER_SLOT?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
