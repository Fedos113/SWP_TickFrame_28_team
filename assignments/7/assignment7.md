\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{graphicx}
\usepackage{geometry}

\geometry{left=1.5cm, right=1.5cm, top=2.5cm, bottom=2.5cm}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    pdftitle={Assignment 6 Week 7 Moodle Submission - Team 28},
}

\begin{document}

% =========================================================================
% HEADER
% =========================================================================
\begin{center}
    {\Large\textbf{INNOPOLIS UNIVERSITY}} \\
    \vspace{0.1cm}
    {\Large\textbf{Software Project (SWP) --- Spring 2026}} \\
    \vspace{0.5cm}
    \textbf{\Large Assignment 6 Week 7 Submission} \\
    \textbf{Sprint 5 (Final Transition \& MVP v3 Delivery)} \\
    \vspace{0.3cm}
    \textbf{Project Name:} SWP TickFrame \quad | \quad \textbf{Team Number:} Team 28 \\
    \textbf{Submission Date:} \today
\end{center}
\vspace{0.5cm}

% =========================================================================
% SECTION 1: TEAM STRUCTURE
% =========================================================================
\section{Team Structure and Technical Responsibilities}

The table below maps the team's Scrum roles and technical ownership for Assignment 6 Week 7 (Sprint 5).

\vspace{0.2cm}
\begin{table}[h!]
    \centering
    \small
    \begin{tabular}{lllll}
        \toprule
        \textbf{Full Name} & \textbf{University Email} & \textbf{GitHub} & \textbf{Scrum Role} & \textbf{Technical Domain} \\
        \midrule
        F. Kozhevnikov & f.kozhevnikov@innopolis.university & \href{https://github.com/Fedos113}{Fedos113} & Product Owner & Backend / Full-stack development \\
        A. Gafarov & a.gafarov@innopolis.university & \href{https://github.com/omarichev}{omarichev} & Developer & Backend / Documentation \\
        A. Mindubaev & a.mindubaev@innopolis.university & \href{https://github.com/pug228}{pug228} & Developer & Quality / CI / Documentation \\
        D. Zhechev & d.zhechev@innopolis.university & \href{https://github.com/DaniilJechev}{DaniilJechev} & Scrum Master & ML engineer / Quant Engineer \\
        M. Bezborodov & m.bezborodov@innopolis.university & \href{https://github.com/MikhailBezborodov024}{MikhailBezborodov024} & Developer & Frontend / UI \\
        \bottomrule
    \end{tabular}
\end{table}

% =========================================================================
% SECTION 2: SUMMARY OF CONTRIBUTIONS
% =========================================================================
\section{Summary of Contributions --- Sprint 5 (Week 7)}

\subsection{F. Kozhevnikov (Fedos113) --- Product Owner / Full-Stack}
\begin{itemize}[leftmargin=*]
    \item Addressed Week 6 customer feedback (e.g., pattern filtering, UI fixes).
    \item Finalized MVP v3 deployment and access instructions.
    \item Updated \texttt{docs/customer-handover.md} to reflect final transition state.
    \item Created final SemVer release for MVP v3.
\end{itemize}

\subsection{A. Gafarov (omarichev) --- Developer / Documentation}
\begin{itemize}[leftmargin=*]
    \item Executed final Week 7 UAT scenarios with customer.
    \item Obtained explicit customer confirmation for handover.
    \item Updated \texttt{README.md}, \texttt{CONTRIBUTING.md}, and \texttt{AGENTS.md}.
    \item Documented final Sprint 5 outcomes in \texttt{reports/week7/README.md}.
\end{itemize}

\subsection{A. Mindubaev (pug228) --- Developer / Quality \& CI}
\begin{itemize}[leftmargin=*]
    \item Verified all acceptance criteria for Sprint 5 PRs.
    \item Maintained CI/CD pipelines and quality gates for MVP v3.
    \item Updated architecture and testing documentation.
\end{itemize}

\subsection{D. Zhechev (DaniilJechev) --- Scrum Master / ML Engineer}
\begin{itemize}[leftmargin=*]
    \item Facilitated Sprint 5 planning and final transition assessment.
    \item Finalized ML microservice integration for MVP v3.
    \item Coordinated Week 7 customer confirmation meeting.
\end{itemize}

\subsection{M. Bezborodov (MikhailBezborodov024) --- Developer / Frontend}
\begin{itemize}[leftmargin=*]
    \item Resolved timeframe switching UI glitches reported in Week 6.
    \item Recorded and published the public sanitized demo video (\textless 2 min).
    \item Updated slide deck for Week 7 lab rehearsal and Week 8 Demo Day.
    \item Finalized Week 7 Moodle PDF submission template.
\end{itemize}

% =========================================================================
% SECTION 3: COMMIT-HASH PERMALINKS
% =========================================================================
\section{Commit-Hash Permalinks}

\subsection{Week 7 Report}
\url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/reports/week7/README.md}

\subsection{Submission commit --- repository tree (Week 7)}
\textit{[INSERT WEEK 7 COMMIT HASH HERE, e.g., https://github.com/.../tree/abc123...]}

% =========================================================================
% SECTION 4: LIVE BOARD AND BACKLOG LINKS
% =========================================================================
\section{Live Board and Backlog Links}

\begin{itemize}[leftmargin=*]
    \item \textbf{Product Backlog:} \url{https://github.com/users/Fedos113/projects/1/views/1}
    \item \textbf{Sprint 5 Backlog (Week 7):} \url{https://github.com/users/Fedos113/projects/1/views/1}
    \item \textbf{Sprint 5 milestone:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/7}
    \item \textbf{Final MVP v3 Release (SemVer):} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v3.0.0}
    \item \textbf{Deployed product (MVP v3):} \url{http://10.93.26.164:8080/}
\end{itemize}

% =========================================================================
% SECTION 5: LIVE DOCUMENTATION LINKS
% =========================================================================
\section{Live Documentation Links (Final State)}

\begin{itemize}[leftmargin=*]
    \item \textbf{docs/customer-handover.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/customer-handover.md}
    \item \textbf{docs/user-acceptance-tests.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/user-acceptance-tests.md}
    \item \textbf{README.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/README.md}
    \item \textbf{CONTRIBUTING.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/CONTRIBUTING.md}
    \item \textbf{AGENTS.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/AGENTS.md}
    \item \textbf{CHANGELOG.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/CHANGELOG.md}
\end{itemize}

% =========================================================================
% SECTION 6: FINAL TRANSITION OUTCOME (Required Part 8)
% =========================================================================
\section{Final Transition Outcome}

\begin{itemize}[leftmargin=*]
    \item \textbf{Handover Level Reached:} Ready for independent use \textit{(or: Independently used by customer)}
    \item \textbf{Customer-Confirmation Status:} Accepted \textit{(or: Accepted with follow-up items)}
    \item \textbf{Follow-up items / Blockers:} None \textit{(or list specific minor items if "Accepted with follow-up")}
    \item \textbf{Evidence:} Private proof of confirmation request provided in Section 11.
\end{itemize}

% =========================================================================
% SECTION 7: CUSTOMER MEETING (WEEK 7)
% =========================================================================
\section{Customer Meeting Recording (Week 7)}

\textbf{Private Link:} \url{[INSERT PRIVATE GOOGLE DRIVE LINK FOR WEEK 7 MEETING]}

\subsection*{Timecodes}
\begin{itemize}[leftmargin=*]
    \item \textbf{Final UAT / Transition Confirmation:} 00:00--15:00
    \item \textbf{Sprint 5 Review (MVP v3):} 15:00--25:00
\end{itemize}

% =========================================================================
% SECTION 8: UAT EXECUTION (WEEK 7)
% =========================================================================
\section{UAT Execution Summary (Week 7)}

\begin{itemize}[leftmargin=*]
    \item \textbf{Date:} [INSERT DATE, e.g., July 17, 2026]
    \item \textbf{Tested:} 9 of 9 scenarios (including Week 6 fixes)
    \item \textbf{Passed:} 9 scenarios
    \item \textbf{Failed:} 0 scenarios
\end{itemize}

% =========================================================================
% SECTION 9: PRIVATE ACCESS INSTRUCTIONS
% =========================================================================
\section{Private Access Instructions (Final MVP v3)}

\begin{itemize}[leftmargin=*]
    \item \textbf{Deployment URL:} \texttt{http://10.93.26.164:8080/}
    \item \textbf{Credentials:} No authentication required
    \item \textbf{Docker Setup:}
\begin{verbatim}
git clone https://github.com/Fedos113/SWP_TickFrame_28_team.git
cd SWP_TickFrame_28_team
git checkout [INSERT WEEK 7 COMMIT HASH]
docker compose up --build
\end{verbatim}
\end{itemize}

% =========================================================================
% SECTION 10: PRESENTATION \& DEMO DAY
% =========================================================================
\section{Presentation \& Demo Day Preparation}

\begin{itemize}[leftmargin=*]
    \item \textbf{Updated Slide deck PDF:} \url{[INSERT UPDATED SLIDE DECK LINK]}
    \item \textbf{Week 7 Lab Rehearsal:} Completed (5-min presentation + 3-min Q\&A)
    \item \textbf{Public Sanitized Demo Video (\textless 2 min):} \url{[INSERT PUBLIC DEMO VIDEO LINK]}
    \item \textbf{Week 8 Demo Day:} Scheduled (7-min presentation + 7-min Q\&A)
\end{itemize}

% =========================================================================
% SECTION 11: INSTRUCTOR-ONLY EVIDENCE
% =========================================================================
\section{Instructor-Only Evidence}

The following evidence is provided only through this Moodle submission:
\begin{itemize}[leftmargin=*]
    \item Customer Meeting recording (Week 7 Final Transition / Sprint Review) --- Section 7 above.
    \item Private proof of transition-confirmation request (e.g., screenshot of customer message exchange): \url{[INSERT SCREENSHOT LINK OR STATE "ATTACHED"]}
    \item Customer consent for recording (obtained verbally).
    \item Private access credentials (if applicable).
\end{itemize}

\clearpage

% =========================================================================
% SECTION 12: CONTRIBUTION TRACEABILITY
% =========================================================================
\section{Sprint 5 Contribution Traceability}

\begin{table}[h!]
\centering
\small
\begin{tabular}{p{2.5cm} p{2cm} p{2cm} p{2cm} p{2.5cm}}
\toprule
\textbf{Team Member} & \textbf{Issues} & \textbf{PRs/MRs} & \textbf{Review Activity} & \textbf{Other Work} \\
\midrule
F. Kozhevnikov & \#130, \#131 & PR \#220, \#221 & Reviewed PR \#222, \#223 & MVP v3 release, final handover docs \\
A. Gafarov & \#132 & PR \#222 & Reviewed PR \#220 & Final UAT, customer confirmation \\
A. Mindubaev & \#133 & PR \#223 & Reviewed PR \#221 & Final CI/CD checks, QA \\
D. Zhechev & \#134 & PR \#224 & Reviewed PR \#224 & ML service finalization, Sprint 5 coordination \\
M. Bezborodov & \#135 & PR \#225 & Reviewed PR \#225 & UI fixes, public demo video, slides \\
\bottomrule
\end{tabular}
\end{table}

\end{document}