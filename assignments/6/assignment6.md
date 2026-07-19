\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{graphicx}
\usepackage{titlesec}
\usepackage{longtable}
\usepackage[left=1cm, right=1cm, top=2.5cm, bottom=2.5cm]{geometry}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    pdftitle={Assignment 6 Moodle Submission Report - Team 28},
}

\titleformat{\section}{\large\bfseries}{\thesection}{1em}{}[\titlerule[0.5pt]]
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{1em}{}

\begin{document}

% =========================================================================
% HEADER
% =========================================================================
\begin{center}
    {\Large\textbf{INNOPOLIS UNIVERSITY}} \\
    \vspace{0.1cm}
    {\Large\textbf{Software Project (SWP) --- Spring 2026}} \\
    \vspace{0.5cm}
    \textbf{Large Assignment 6: MVP v3 \& Customer Handover Report} \\
    \vspace{0.3cm}
    \textbf{Project Name:} SWP TickFrame \quad \| \quad \textbf{Team Number:} Team 28 \\
    \textbf{Submission Date:} \today \\
    \textbf{Reporting Period:} Sprint 5 (Week 6) \& Sprint 6 (Week 7)
\end{center}
\vspace{0.5cm}

% =========================================================================
% SECTION 1: TEAM STRUCTURE & TECHNICAL RESPONSIBILITIES
% =========================================================================
\section{Team Structure and Technical Responsibilities}
The table below maps the team's Scrum roles and technical ownership for Assignment 6 (Sprints 5--6).
\vspace{0.2cm}

\begin{table}[h!]
\centering
\small
\begin{tabular}{lllll}
\toprule
\textbf{Full Name} & \textbf{University Email} & \textbf{GitHub} & \textbf{Scrum Role} & \textbf{Technical Domain} \\
\midrule
F.~Kozhevnikov & f.kozhevnikov@innopolis.university & \href{https://github.com/Fedos113}{Fedos113} & Product Owner & Backend / Frontend / Architecture / CI \\
A.~Gafarov & a.gafarov@innopolis.university & \href{https://github.com/omarichev}{omarichev} & Developer & Backend / Documentation / Reports \\
A.~Mindubaev & a.mindubaev@innopolis.university & \href{https://github.com/pug228}{pug228} & Developer & Quality / CI / Testing \\
D.~Zhechev & d.zhechev@innopolis.university & \href{https://github.com/DaniilJechev}{DaniilJechev} & Scrum Master & ML / Quant Engineering \\
M.~Bezborodov & m.bezborodov@innopolis.university & \href{https://github.com/MikhailBezborodov024}{MikhailBezborodov024} & Developer & Frontend / UI \\
\bottomrule
\end{tabular}
\end{table}

% =========================================================================
% SECTION 2: SUMMARY OF CONTRIBUTIONS
% =========================================================================
\section{Summary of Contributions --- Sprints 5 \& 6}

\subsection{F.~Kozhevnikov (Fedos113) --- Product Owner / Full-Stack}
\begin{itemize}[leftmargin=*]
    \item \textbf{Sprint 5 (Week 6):}
    \begin{itemize}
        \item Repository scaffolding for Assignment 6 and delivery plans.
        \item Week 6 trial release preparation and deployment.
        \item Customer handover documentation initial draft.
        \item Transition readiness meeting coordination.
    \end{itemize}
    \item \textbf{Sprint 6 (Week 7):}
    \begin{itemize}
        \item MVP v3 final release and deployment.
        \item Incorporation of Week 6 trial feedback.
        \item Final customer handover completion.
        \item Demo Day presentation preparation.
    \end{itemize}
\end{itemize}

\subsection{A.~Gafarov (omarichev) --- Developer / Documentation}
\begin{itemize}[leftmargin=*]
    \item \textbf{Sprint 5 (Week 6):}
    \begin{itemize}
        \item UAT scenarios update for MVP v3.
        \item Week 6 trial UAT execution with customer.
        \item Customer feedback documentation.
    \end{itemize}
    \item \textbf{Sprint 6 (Week 7):}
    \begin{itemize}
        \item Final UAT execution and confirmation.
        \item Customer acceptance confirmation.
        \item Week 7 report finalization.
    \end{itemize}
\end{itemize}

\subsection{A.~Mindubaev (pug228) --- Developer / Quality \& CI}
\begin{itemize}[leftmargin=*]
    \item \textbf{Sprint 5 (Week 6):}
    \begin{itemize}
        \item CI/CD pipeline updates for trial release.
        \item Testing documentation maintenance.
        \item Architecture documentation updates.
    \end{itemize}
    \item \textbf{Sprint 6 (Week 7):}
    \begin{itemize}
        \item Final testing and QA for MVP v3.
        \item SemVer release creation.
        \item Documentation finalization.
    \end{itemize}
\end{itemize}

\subsection{D.~Zhechev (DaniilJechev) --- Scrum Master / ML Engineer}
\begin{itemize}[leftmargin=*]
    \item \textbf{Sprint 5 (Week 6):}
    \begin{itemize}
        \item Sprint 5 planning and coordination.
        \item ML microservice maintenance.
        \item Transition readiness assessment.
    \end{itemize}
    \item \textbf{Sprint 6 (Week 7):}
    \begin{itemize}
        \item Sprint 6 execution and monitoring.
        \item Final product transition coordination.
        \item Demo Day rehearsal facilitation.
    \end{itemize}
\end{itemize}

\subsection{M.~Bezborodov (MikhailBezborodov024) --- Developer / Frontend}
\begin{itemize}[leftmargin=*]
    \item \textbf{Sprint 5 (Week 6):}
    \begin{itemize}
        \item Week 6 trial release frontend polish.
        \item UI/UX improvements based on feedback.
        \item Assignment 6 Moodle PDF template creation.
    \end{itemize}
    \item \textbf{Sprint 6 (Week 7):}
    \begin{itemize}
        \item MVP v3 frontend finalization.
        \item Public demo video recording (\textless 2 min).
        \item Demo Day presentation slides.
    \end{itemize}
\end{itemize}

% =========================================================================
% SECTION 3: COMMIT-HASH PERMALINKS
% =========================================================================
\section{Commit-Hash Permalinks}

\subsection{reports/week6/README.md (Sprint 5)}
\url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/reports/week6/README.md}

\subsection{reports/week7/README.md (Sprint 6)}
\url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/reports/week7/README.md}

\subsection{Submission commit --- repository tree (Week 6)}
\textit{[Add commit hash after Week 6 submission]}

\subsection{Submission commit --- repository tree (Week 7)}
\textit{[Add commit hash after Week 7 submission]}

% =========================================================================
% SECTION 4: LIVE BOARD AND BACKLOG LINKS
% =========================================================================
\section{Live Board and Backlog Links}

\begin{itemize}[leftmargin=*]
    \item \textbf{Product Backlog board/view:} \
          \url{https://github.com/users/Fedos113/projects/1/views/1}

    \item \textbf{Sprint 5 Backlog (Week 6):} \
          \url{https://github.com/users/Fedos113/projects/1/views/1}

    \item \textbf{Sprint 6 Backlog (Week 7):} \
          \url{https://github.com/users/Fedos113/projects/1/views/1}

    \item \textbf{Sprint 5 milestone:} \
          \url{https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/6}

    \item \textbf{Sprint 6 milestone:} \
          \url{https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/7}

    \item \textbf{Week 6 Trial Release (SemVer):} \
          \textit{[Add release link after Week 6]}

    \item \textbf{MVP v3 Final Release (SemVer):} \
          \textit{[Add release link after Week 7 - must have higher precedence than Week 6]}

    \item \textbf{Deployed product (Week 6 Trial):} \
          \url{http://10.93.26.164:8080/}

    \item \textbf{Deployed product (MVP v3 - Week 7):} \
          \url{http://10.93.26.164:8080/}

    \item \textbf{Public sanitized demo video (\textless 2 min):} \
          \textit{[Add link after Week 7]}
\end{itemize}

% =========================================================================
% SECTION 5: LIVE DOCUMENTATION LINKS
% =========================================================================
\section{Live Documentation Links (Assignment 6 Maintained Assets)}

\begin{itemize}[leftmargin=*]
    \item \textbf{docs/customer-handover.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/customer-handover.md}
    \item \textbf{docs/roadmap.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/roadmap.md}
    \item \textbf{docs/user-acceptance-tests.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/user-acceptance-tests.md}
    \item \textbf{README.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/README.md}
    \item \textbf{CONTRIBUTING.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/CONTRIBUTING.md}
    \item \textbf{AGENTS.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/AGENTS.md}
    \item \textbf{CHANGELOG.md:} \url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/CHANGELOG.md}
\end{itemize}

% =========================================================================
% SECTION 6: SPRINT 5 (WEEK 6) DELIVERABLES
% =========================================================================
\section{Sprint 5 (Week 6) Deliverables}

\subsection{Trial Release Status}
\begin{itemize}
    \item \textbf{Release Version:} [e.g., v3.0.0-trial]
    \item \textbf{SemVer Release:} \textit{[Add link]}
    \item \textbf{Access Instructions:} See Section 11 below
    \item \textbf{Stability:} Trial/handover-candidate release
\end{itemize}

\subsection{Transition Readiness Summary}
\begin{itemize}
    \item \textbf{Meeting Date:} [Date of Week 6 transition meeting]
    \item \textbf{Customer Trial:} [Independent use / Deployed by customer / Not yet deployed]
    \item \textbf{Readiness Level:} [Ready for independent use / Partially ready / Not ready]
    \item \textbf{Blockers Identified:} [List or "None"]
\end{itemize}

\subsection{Customer Feedback Response Table}
\begin{table}[h!]
\centering
\small
\begin{tabular}{p{4cm} p{3cm} p{4cm}}
\toprule
\textbf{Feedback Item} & \textbf{Priority} & \textbf{Action (Sprint 6)} \\
\midrule
Feedback 1 & High/Med/Low & PBI \#XXX \\
Feedback 2 & High/Med/Low & PBI \#XXX \\
\bottomrule
\end{tabular}
\end{table}

% =========================================================================
% SECTION 7: SPRINT 6 (WEEK 7) DELIVERABLES
% =========================================================================
\section{Sprint 6 (Week 7) Deliverables}

\subsection{MVP v3 Final Release}
\begin{itemize}
    \item \textbf{Release Version:} v3.0.0 (or higher)
    \item \textbf{SemVer Release:} \textit{[Add link]}
    \item \textbf{Mapped to Milestone:} Sprint 6
    \item \textbf{Public Demo Video:} \textit{[Add link]}
\end{itemize}

\subsection{Final Transition Outcome}
\begin{itemize}
    \item \textbf{Handover Level:} 
    \begin{itemize}
        \item[$\circ$] Ready for independent use
        \item[$\circ$] Independently used by customer
        \item[$\circ$] Deployed/operated on customer side
    \end{itemize}
    
    \item \textbf{Customer Confirmation Status:}
    \begin{itemize}
        \item[$\circ$] Accepted
        \item[$\circ$] Accepted with follow-up items
        \item[$\circ$] Not yet accepted
    \end{itemize}
    
    \item \textbf{docs/customer-handover.md Acceptance:} [Accepted / Pending]
\end{itemize}

\subsection{Follow-Up Maintenance Items}
\begin{itemize}
    \item [List items addressed in Sprint 6]
\end{itemize}

% =========================================================================
% SECTION 8: REVIEWED ISSUE-LINKED PRs
% =========================================================================
\section{Reviewed Issue-Linked PRs / MRs (Sprints 5--6 Evidence)}

\subsection{Sprint 5 (Week 6) PRs}
\begin{itemize}[leftmargin=*]
    \item \textbf{PR \#[XXX]:} [Description] \
          \textbf{Closes issues:} \#[...]. \
          \textbf{Author:} [Name]. \
          \textbf{Reviewer:} [Name] --- APPROVED. \
          \url{[PR link]}
\end{itemize}

\subsection{Sprint 6 (Week 7) PRs}
\begin{itemize}[leftmargin=*]
    \item \textbf{PR \#[XXX]:} [Description] \
          \textbf{Closes issues:} \#[...]. \
          \textbf{Author:} [Name]. \
          \textbf{Reviewer:} [Name] --- APPROVED. \
          \url{[PR link]}
\end{itemize}

% =========================================================================
% SECTION 9: CUSTOMER MEETING RECORDINGS
% =========================================================================
\section{Customer Meeting Recordings}

\subsection{Week 6: UAT / Transition Readiness / Sprint Review}
\textbf{Recording link (instructor access only):} \
\textit{[Add private Google Drive/OneDrive link]}

\textbf{Timecodes:}
\begin{itemize}
    \item \textbf{UAT session:} \texttt{00:00--XX:XX} --- customer tested Week 6 trial
    \item \textbf{Transition discussion:} \texttt{XX:XX--XX:XX} --- readiness assessment
    \item \textbf{Sprint Review:} \texttt{XX:XX--XX:XX} --- feedback and action items
\end{itemize}

\subsection{Week 7: Final Transition / Sprint Review}
\textbf{Recording link (instructor access only):} \
\textit{[Add private Google Drive/OneDrive link]}

\textbf{Timecodes:}
\begin{itemize}
    \item \textbf{Final UAT:} \texttt{00:00--XX:XX} --- MVP v3 validation
    \item \textbf{Transition confirmation:} \texttt{XX:XX--XX:XX} --- handover acceptance
    \item \textbf{Sprint Review:} \texttt{XX:XX--XX:XX} --- final feedback
\end{itemize}

% =========================================================================
% SECTION 10: PRESENTATION \& DEMO DAY
% =========================================================================
\section{Presentation \& Demo Day}

\subsection{Week 6 Moodle Submission}
\begin{itemize}
    \item \textbf{Slide deck PDF:} \textit{[Attached or linked]}
    \item \textbf{Rehearsed presentation video:} \textit{[Private link - must show team standing]}
\end{itemize}

\subsection{Week 7 Lab Rehearsal}
\begin{itemize}
    \item \textbf{Date:} [Date]
    \item \textbf{Duration:} 5-min presentation + 3-min Q\&A
    \item \textbf{Status:} [Completed / Scheduled]
\end{itemize}

\subsection{Week 8 Demo Day}
\begin{itemize}
    \item \textbf{Duration:} 7-min presentation + 7-min Q\&A
    \item \textbf{Pre-recorded demo:} \textless 2 minutes (no live demos)
    \item \textbf{Demo video link:} \textit{[Add link]}
    \item \textbf{Q\&A assignments:} [Who answers which topics]
\end{itemize}

% =========================================================================
% SECTION 11: MVP v3 ACCESS INSTRUCTIONS
% =========================================================================
\section{MVP v3 Access Instructions}

\subsection{Docker Deployment (Recommended)}
\begin{enumerate}[leftmargin=*]
    \item Clone the repository at the submission commit:
\begin{verbatim}
git clone https://github.com/Fedos113/SWP_TickFrame_28_team.git
cd SWP_TickFrame_28_team
git checkout [COMMIT_HASH]
\end{verbatim}
    \item Copy the environment template:
\begin{verbatim}
cp .env.example .env
\end{verbatim}
    \item Build and run with Docker Compose:
\begin{verbatim}
docker compose up --build
\end{verbatim}
    \item Open \texttt{http://localhost:8080} in a browser.
\end{enumerate}

\subsection{Verification Checklist}
\begin{itemize}
    \item Application loads successfully
    \item Real-time data streaming works
    \item All MVP v3 features functional
    \item Documentation accessible
\end{itemize}

% =========================================================================
% SECTION 12: PRIVATE ACCESS INSTRUCTIONS
% =========================================================================
\section{Private Access Instructions}

\begin{itemize}
    \item \textbf{Week 6 Trial Deployment URL:} \texttt{http://10.93.26.164:8080/}
    \item \textbf{MVP v3 Deployment URL:} \texttt{http://10.93.26.164:8080/}
    \item \textbf{Credentials:} [If any, otherwise "No authentication required"]
    \item \textbf{Environment Variables:} See \texttt{docs/customer-handover.md}
\end{itemize}

% =========================================================================
% SECTION 13: INSTRUCTOR-ONLY EVIDENCE
% =========================================================================
\section{Instructor-Only Evidence}

The following evidence is not committed to the public repository:
\begin{itemize}
    \item Customer UAT and Sprint Review recordings (Week 6 \& Week 7)
    \item Rehearsed presentation video (private link)
    \item Customer consent for recording (obtained verbally)
    \item Proof of transition confirmation (screenshots of customer messages)
    \item Private access credentials (if applicable)
\end{itemize}

% =========================================================================
% SECTION 14: RETROSPECTIVES \& REFLECTIONS
% =========================================================================
\section{Retrospectives \& Reflections}

\subsection{Sprint 5 Retrospective (Week 6)}
\texttt{reports/week6/retrospective.md} \\
\url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/reports/week6/retrospective.md}

\subsection{Sprint 6 Retrospective (Week 7)}
\texttt{reports/week7/retrospective.md} \\
\url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/reports/week7/retrospective.md}

\subsection{Week 6 Reflection}
\texttt{reports/week6/reflection.md} \\
\url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/reports/week6/reflection.md}

\subsection{Week 7 Reflection}
\texttt{reports/week7/reflection.md} \\
\url{https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/reports/week7/reflection.md}

\subsection{LLM Usage Reports}
\begin{itemize}
    \item \textbf{Week 6:} \texttt{reports/week6/llm-report.md}
    \item \textbf{Week 7:} \texttt{reports/week7/llm-report.md}
\end{itemize}

\end{document}