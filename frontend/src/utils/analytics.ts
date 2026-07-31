const MEASUREMENT_ID = 'G-SB70DGPRLJ'

export const trackPageView = (pagePath: string, pageTitle: string) => {
  window.gtag?.('event', 'page_view', {
    send_to: MEASUREMENT_ID,
    page_path: pagePath,
    page_location: window.location.href,
    page_title: pageTitle,
  })
}

export const trackMetaPageView = () => {
  window.fbq?.('track', 'PageView')
}
