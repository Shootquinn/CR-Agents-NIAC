## Score rubric (Step A, scale 1 to 5)
Source: SOL p.20-21. Four weighted criteria. Sum: 100.

| criterion | weight |
|---|---|
| Innovation | 30 |
| Impact | 30 |
| Mission | 20 |
| Technical Approach | 20 |

### Innovation (SOL p.20)
1. No clearly innovative concept, or no justification of feasibility.
2. May be new enough to need feasibility analysis; justification is superficial.
3. Appears new enough to need analysis; reasonable justification of feasibility.
4. Clearly novel and unexplored; credible justification of feasibility.
5. Clearly novel and unexplored; solid justification of feasibility.

### Impact (SOL p.20)
1. No adequate benefit over reasonable alternatives, or no back-of-the-envelope support.
2. May offer benefit; back-of-the-envelope support is insufficient.
3. Appears to offer potential benefit; reasonable back-of-the-envelope estimate.
4. Clearly offers significant benefit; credible back-of-the-envelope estimate.
5. Clearly offers significant benefit; solid back-of-the-envelope estimate.

### Mission (SOL p.20-21)
1. No adequate mission in enough detail to assess feasibility and benefit.
2. More than one mission, and it is unclear which one is examined.
3. A single specific mission and architecture; detail may suffice to show feasibility and benefit.
4. A single significant mission and architecture; detail likely suffices.
5. A single specific mission and architecture; detail clearly suffices.

### Technical Approach (SOL p.21)
1. Work plan outline shows no grasp of major issues and no reasonable course of study.
2. Outline does not adequately show grasp of major issues.
3. Adequate outline; grasp of major issues; reasonable course of study.
4. Good outline; clear grasp of major issues; credible course of study.
5. Outline with clear grasp of major issues and a convincing course of study for one representative mission.

### Scoring row form
`| criterion | score 1-5 | quote <= 15 words |`

### Weighted score
Formula: `weighted = (30*I + 30*P + 20*M + 20*T) / 100`. The scorer never does arithmetic. The orchestrator runs this command with the four scores in place of 4, 3, 5, 2 (Innovation, Impact, Mission, Technical Approach):

`python -c "i,p,m,t=4,3,5,2; print((30*i+30*p+20*m+20*t)/100)"`

Invite threshold: weighted 3 or better (SOL p.21).

Worked hand case: scores 4, 3, 5, 2 give 3.5.
