// Theorem environments for FMF paper
// Each environment: colored left border, label, numbered Section.N
// Updated for Typst 0.14+ (context instead of locate)

#let theorem-counter = counter("theorem")
#let lemma-counter = counter("lemma")

#let _env(body, name: "", label-color: rgb("#1a5276"), fill-color: rgb("#f8f9fa"), number: none) = {
  block(
    width: 100%,
    inset: (left: 12pt, right: 10pt, top: 8pt, bottom: 8pt),
    stroke: (left: 3pt + label-color),
    fill: fill-color,
    [
      #if number != none [
        *#name #number.*
      ] else [
        *#name.*
      ]
      #body
    ],
  )
}

#let theorem(body, name: none) = {
  theorem-counter.step()
  context {
    let num = theorem-counter.get()
    let sec = counter(heading).get()
    let label = if sec.len() > 0 { str(sec.first()) + "." + str(num.first()) } else { str(num.first()) }
    let title = if name != none { "Theorem " + label + " (" + name + ")" } else { "Theorem " + label }
    _env(body, name: title, label-color: rgb("#1a5276"), fill-color: rgb("#eaf2f8"))
  }
}

#let proposition(body, name: none) = {
  theorem-counter.step()
  context {
    let num = theorem-counter.get()
    let sec = counter(heading).get()
    let label = if sec.len() > 0 { str(sec.first()) + "." + str(num.first()) } else { str(num.first()) }
    let title = if name != none { "Proposition " + label + " (" + name + ")" } else { "Proposition " + label }
    _env(body, name: title, label-color: rgb("#6c3483"), fill-color: rgb("#f5eef8"))
  }
}

#let lemma(body, name: none) = {
  lemma-counter.step()
  context {
    let num = lemma-counter.get()
    let sec = counter(heading).get()
    let label = if sec.len() > 0 { str(sec.first()) + "." + str(num.first()) } else { str(num.first()) }
    let title = if name != none { "Lemma " + label + " (" + name + ")" } else { "Lemma " + label }
    _env(body, name: title, label-color: rgb("#1e8449"), fill-color: rgb("#eafaf1"))
  }
}

#let observation(body, name: none) = {
  theorem-counter.step()
  context {
    let num = theorem-counter.get()
    let sec = counter(heading).get()
    let label = if sec.len() > 0 { str(sec.first()) + "." + str(num.first()) } else { str(num.first()) }
    let title = if name != none { "Observation " + label + " (" + name + ")" } else { "Observation " + label }
    _env(body, name: title, label-color: rgb("#b7950b"), fill-color: rgb("#fef9e7"))
  }
}

#let conjecture(body, name: none) = {
  theorem-counter.step()
  context {
    let num = theorem-counter.get()
    let sec = counter(heading).get()
    let label = if sec.len() > 0 { str(sec.first()) + "." + str(num.first()) } else { str(num.first()) }
    let title = if name != none { "Conjecture " + label + " (" + name + ")" } else { "Conjecture " + label }
    _env(body, name: title, label-color: rgb("#c0392b"), fill-color: rgb("#fdedec"))
  }
}

#let definition(body, name: none) = {
  let title = if name != none { "Definition (" + name + ")" } else { "Definition" }
  _env(body, name: title, label-color: rgb("#566573"), fill-color: rgb("#f2f3f4"))
}

#let proof(body) = {
  block(
    width: 100%,
    inset: (left: 12pt, top: 4pt, bottom: 4pt),
    [_Proof._ #body #h(1fr) $square$],
  )
}

#let remark(body) = {
  block(
    width: 100%,
    inset: (left: 12pt, top: 4pt, bottom: 4pt),
    [_Remark._ #body],
  )
}
