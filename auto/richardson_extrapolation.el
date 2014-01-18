(TeX-add-style-hook "richardson_extrapolation"
 (lambda ()
    (LaTeX-add-labels
     "eq:f^*(x)"
     "eq:f(h)"
     "eq:n:equation"
     "eq:alpha:equation"
     "eq:true:solution")
    (TeX-add-symbols
     "R"
     "eval")
    (TeX-run-style-hooks
     "hyperref"
     "listings"
     "braket"
     "verbatim"
     "mathrsfs"
     "graphicx"
     "latexsym"
     "amssymb"
     "amsmath"
     "fullpage"
     "latex2e"
     "art10"
     "article")))

