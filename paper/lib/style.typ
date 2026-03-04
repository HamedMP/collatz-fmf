// Page layout and styling for FMF paper

#let paper-style(doc) = {
  set page(
    paper: "a4",
    margin: (top: 3cm, bottom: 3cm, left: 2.5cm, right: 2.5cm),
    numbering: "1",
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: rgb("#666"))
        _Elementary Exponential Density Bounds for Collatz Growth Chains_
        #h(1fr)
        #counter(page).display()
      ]
    },
  )

  set text(
    font: "New Computer Modern",
    size: 11pt,
    lang: "en",
  )

  set par(
    justify: true,
    leading: 0.65em,
    first-line-indent: 1.5em,
  )

  set heading(numbering: "1.")
  show heading.where(level: 1): it => {
    set text(size: 14pt)
    v(1.5em)
    it
    v(0.5em)
  }
  show heading.where(level: 2): it => {
    set text(size: 12pt)
    v(1em)
    it
    v(0.3em)
  }

  set math.equation(numbering: "(1)")

  set bibliography(style: "springer-mathphys")

  doc
}

#let title-page(title: "", subtitle: "", authors: (), date: "", abstract: "") = {
  set par(first-line-indent: 0pt)
  align(center)[
    #v(2cm)
    #text(size: 18pt, weight: "bold")[#title]
    #v(0.5em)
    #if subtitle != "" [
      #text(size: 13pt, fill: rgb("#444"))[#subtitle]
      #v(1em)
    ]
    #for author in authors [
      #text(size: 12pt)[#author] \
    ]
    #v(0.5em)
    #text(size: 10pt, fill: rgb("#666"))[#date]
    #v(1.5em)
  ]

  if abstract != "" {
    align(center)[
      #set par(first-line-indent: 0pt)
      #block(
        width: 85%,
        inset: (x: 0pt),
      )[
        #align(center)[*Abstract*]
        #v(0.3em)
        #set text(size: 10pt)
        #abstract
      ]
    ]
  }

  v(1em)
  line(length: 100%, stroke: 0.5pt + rgb("#ccc"))
  pagebreak()
}
