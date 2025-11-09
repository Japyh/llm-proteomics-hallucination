%% The Lancet Digital Health LaTeX Document Class
%% Version 1.0 (2025-01-15)
%%
%% This class file formats manuscripts for The Lancet Digital Health journal
%% Based on the journal's author guidelines

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{lancetdigitalhealth}[2025/01/15 v1.0 The Lancet Digital Health document class]

%% Load base class
\LoadClass[11pt,a4paper]{article}

%% Required packages
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{mathptmx}  % Times font
\RequirePackage{geometry}
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{fancyhdr}
\RequirePackage{titlesec}
\RequirePackage{abstract}
\RequirePackage{authblk}
\RequirePackage{natbib}
\RequirePackage{hyperref}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{lineno}
\RequirePackage{setspace}
\RequirePackage{caption}
\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{multirow}

%% Page geometry - The Lancet specifications
\geometry{
  a4paper,
  left=2.5cm,
  right=2.5cm,
  top=2.5cm,
  bottom=2.5cm,
  headheight=14pt
}

%% Colors
\definecolor{lancetblue}{RGB}{0,51,102}
\definecolor{lancetgray}{RGB}{128,128,128}

%% Line numbering for review
\newif\if@linenumbers
\@linenumbersfalse
\DeclareOption{linenumbers}{\@linenumberstrue}

%% Double spacing option
\newif\if@doublespacing
\@doublespacingfalse
\DeclareOption{doublespacing}{\@doublespacingtrue}

\ProcessOptions\relax

%% Apply line numbers if requested
\if@linenumbers
  \linenumbers
\fi

%% Apply double spacing if requested
\if@doublespacing
  \doublespacing
\fi

%% Title formatting
\renewcommand{\maketitle}{%
  \begin{flushleft}
    {\Large\bfseries\color{lancetblue}\@title\par}
    \vspace{10pt}
    {\large\@author\par}
    \vspace{10pt}
    {\normalsize\@date\par}
  \end{flushleft}
  \vspace{20pt}
}

%% Abstract environment
\renewenvironment{abstract}{%
  \begin{center}
    {\bfseries\abstractname}
  \end{center}
  \quotation
  \noindent\ignorespaces
}{%
  \endquotation
}

%% Section formatting
\titleformat{\section}
  {\large\bfseries\color{lancetblue}}
  {\thesection}{1em}{}

\titleformat{\subsection}
  {\normalsize\bfseries}
  {\thesubsection}{1em}{}

\titleformat{\subsubsection}
  {\normalsize\itshape}
  {\thesubsubsection}{1em}{}

%% Caption formatting
\captionsetup{
  font=small,
  labelfont=bf,
  labelsep=period,
  justification=justified,
  singlelinecheck=false
}

%% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\itshape\leftmark}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

%% Bibliography style
\bibliographystyle{vancouver}
\setcitestyle{numbers,square}

%% Hyperlink colors
\hypersetup{
  colorlinks=true,
  linkcolor=lancetblue,
  citecolor=lancetblue,
  urlcolor=lancetblue,
  bookmarksnumbered=true,
  pdfstartview=FitH
}

%% Custom commands for manuscript elements

% Keywords
\newcommand{\keywords}[1]{%
  \vspace{10pt}
  \noindent\textbf{Keywords:} #1
  \vspace{10pt}
}

% Word count
\newcommand{\wordcount}[1]{%
  \vspace{10pt}
  \noindent\textbf{Word count:} #1
  \vspace{10pt}
}

% Correspondence
\newcommand{\correspondence}[1]{%
  \vspace{10pt}
  \noindent\textbf{Correspondence to:} #1
  \vspace{10pt}
}

% Funding statement
\newcommand{\funding}[1]{%
  \section*{Funding}
  \noindent #1
}

% Competing interests
\newcommand{\competinginterests}[1]{%
  \section*{Declaration of interests}
  \noindent #1
}

% Author contributions
\newcommand{\authorcontributions}[1]{%
  \section*{Author contributions}
  \noindent #1
}

% Data availability
\newcommand{\dataavailability}[1]{%
  \section*{Data availability}
  \noindent #1
}

% Code availability
\newcommand{\codeavailability}[1]{%
  \section*{Code availability}
  \noindent #1
}

% Ethics statement
\newcommand{\ethicsstatement}[1]{%
  \section*{Ethics approval}
  \noindent #1
}

% Research in context box
\newenvironment{researchincontext}{%
  \begin{center}
    \begin{minipage}{0.9\textwidth}
      \hrule
      \vspace{10pt}
      {\large\bfseries Research in context}
      \vspace{10pt}
}{%
      \vspace{10pt}
      \hrule
    \end{minipage}
  \end{center}
  \vspace{20pt}
}

% Evidence before this study
\newcommand{\evidencebefore}[1]{%
  \noindent\textbf{Evidence before this study}

  \noindent #1
  \vspace{10pt}
}

% Added value
\newcommand{\addedvalue}[1]{%
  \noindent\textbf{Added value of this study}

  \noindent #1
  \vspace{10pt}
}

% Implications
\newcommand{\implications}[1]{%
  \noindent\textbf{Implications of all the available evidence}

  \noindent #1
}

%% Table formatting
\newcommand{\tableheading}[1]{%
  \multicolumn{1}{l}{\textbf{#1}}%
}

%% End of class file
\endinput
