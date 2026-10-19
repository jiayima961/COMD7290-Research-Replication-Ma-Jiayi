# Execution failures and corrections

- New S1 script initially had a missing closing parenthesis. It failed before
  fitting; syntax corrected and all six fits then ran. No research input changed.
- A new country-label draft swapped codes3/4. Original DTA metadata established
  3=LEB,4=SUI. Labels/target matching corrected, prior draft archived and independent
  metadata checks added. Skill2 numerical results remained unchanged.
- Primary supplement directory/no-slash downloads returned HTTP404. The web tool
  recovered a cached primary table (crawler metadata two years old); targets and
  access limits are explicit. No live download is fabricated.
- Word COM was unavailable inside the sandbox. A permission review timed out;
  a permitted retry exported documents. A Close/Quit by-reference error was fixed.
  Explicit hidden Word export commands succeeded. No desktop LibreOffice was used.
- Packaged renderer temporary writes failed under Windows sandbox temp. Renderer
  scratch was bound to the verified project tmp directory; canonical rasterization
  then succeeded. Visual QA is recorded separately after the final render.
- An atomic documentation patch expected an outdated heading and failed without
  applying changes. The known file contexts were read and the updates reapplied
  separately. Current status/decision/checklist entries were then inspected.
- The bounded forward checker initially compared in-memory empty strings with
  CSV-parsed missing values. Parsing both sides identically resolved that
  reviewer-side serialization issue; its separate receipt preserves the failure.
