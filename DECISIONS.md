## Reicht ein Commit-Kommentar – oder gehört das in DECISIONS.md?
> Faustregel: Wenn du es jemand anderem erklären müsstest → rein damit.
> Dokumentiert wird: Was? Und Warum?

## [2025-05-25]
**Yakoon als Solution **
Yakoon ist nun Solution
> Platform -> Solution -> (Entry-points)
> In Solution finden die Lösung statt
> später: yakoon init solution my-app; yakoon dev; yakoon deploy --docker

## [2025-05-24]
**Webclient - React & VITE **
Der Webzugriff wurde mit React realisiert. 
> Modern und super schnell in der Entwicklung. Zudem stabil im Dev-Livecycle.
> Dark-Design
> npm run dev

## [2025-05-24]
**Version & Git & Docker**
Die Version der Platform wird über Git-Tags abgefragt. Der Fallback ist Datei (version.txt)
> version.txt wird später beim docker build geschrieben und version.txt verwendet.
> git tag -a v0.3.1 -m "Yakoon version 0.3.1"
