## SPECIAL RULE FOR UICONTROL TAGS (memoQ bilingual DOCX)

- Text wrapped in `[uicontrol...{uicontrol]` tags must be translated with the original text followed by translation in parentheses. This is extremely important  and must always be done.
- **Structure**: `[uicontrol id="GUID"}Original English Text{uicontrol]: Description`
- **Translation format**: `[uicontrol id="GUID"}Original English Text (Translation){uicontrol]: Translated Description
• **Note**: if this rule would result in something like: "Test (Test)"` (i.e, Where the source and target language are identical),  you can skip the rule and just write: "Test".

### Example 1:
- **Source**: `[uicontrol id="GUID-D82B8555-1166-4740-AFD1-78FCA44BF83A"}Turn on the positioning mode{uicontrol]: Enabling the function of camera-aided positioning.`
- **Target**: `[uicontrol id="GUID-D82B8555-1166-4740-AFD1-78FCA44BF83A"}Turn on the positioning mode (Schakel de positioneringsmodus in){uicontrol]: Het inschakelen van de functie voor camera-ondersteunde positionering.`
- **CRITICAL**: Keep the original English text unchanged, add translation in parentheses after it

### Example 2:
- **Source**: Click the [uicontrol id="GUID-328189DB-A480-4BEE-822E-7AABB5EC4C8B"}Reference Line Group{uicontrol] icon [image cid="OP7aT" href="GUID-D423EB26-7B46-4643-A174-1F600C671EDB"].
- **Target**: Klik op het pictogram [uicontrol id="GUID-328189DB-A480-4BEE-822E-7AABB5EC4C8B"}Reference Line Group (Referentielijngroep){uicontrol] icon [image cid="OP7aT" href="GUID-D423EB26-7B46-4643-A174-1F600C671EDB"].
- **CRITICAL**: Keep the original English text unchanged, add translation in parentheses after it.

# Special rule for Non-translatables:
Treat all things you come across like: "SopClass" as non-translatables. That is, do not translate them, merely transfer them to the target text untouched.
