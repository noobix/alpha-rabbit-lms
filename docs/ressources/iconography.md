---
Author: Kelvin Kabute
Last-updated: 2026-10-25
---

To create a world-class, intuitive UI for your Library Management System, icons shouldn't just be static pictures—they need to communicate **state, severity, and intent** through motion and color.

Below is the **Animation & Interaction Design System** tailored to your Phosphor Icons. I have categorized the animations based on the **severity of the action** (Constructive, Destructive, Warning, System) and blended them with **hover behaviors and color psychology** (using your Ghana-inspired palette: `ghanaGreen`, `ghanaGold`, `ghanaRed`).

---

### 🎨 The Animation & Interaction Design System

Before diving into the matrix, here are the rules your AI assistant should follow when generating these components in VS Code:

| Action Profile       | Severity          | Animation Style                  | Hover Color & Behavior                                                              | UX Psychology                                                            |
| :------------------- | :---------------- | :------------------------------- | :---------------------------------------------------------------------------------- | :----------------------------------------------------------------------- |
| **Constructive**     | Low / Positive    | **Draw-in, Scale-up, Fill-swap** | `ghanaGreen` / `ghanaGold`. Icon fills or grows smoothly.                           | Reinforces success, creation, and safe actions.                          |
| **Destructive**      | High / Negative   | **Shake, Fade, Stamp**           | `ghanaRed`. Icon shakes on hover to warn the user before clicking.                  | Prevents accidental clicks; signals irreversible or blocking actions.    |
| **Warning / Alert**  | Medium / Critical | **Pulse, Bounce, Ripple**        | `Amber` / `Orange`. Subtle pulsing or bouncing draws the eye without causing panic. | Highlights climate risks, degradation, or anomalies requiring attention. |
| **System / Process** | Neutral / Active  | **Spin, Sweep, Unfold**          | `Blue` / `Cyan`. Continuous or triggered mechanical motion.                         | Indicates background tasks, syncing, scanning, or structural changes.    |
| **Informational**    | Low / Passive     | **Tilt, Slide, Morph**           | `Gray` → `Blue`. Subtle shifts that acknowledge user presence.                      | Guides the user without demanding immediate action.                      |

---

### 📚 1. Security, Governance & System Admin

_Focus: Privacy, Authority, and System Integrity_

| Entity / Action       | Phosphor Icon            | Animation Style     | Hover State & Color                               | Severity & UX Context                                                |
| :-------------------- | :----------------------- | :------------------ | :------------------------------------------------ | :------------------------------------------------------------------- |
| **Add Staff**         | `UserPlus`               | **Pop-in & Draw**   | `ghanaGreen` fill. The `+` draws itself.          | **Constructive**. Welcoming, clear creation action.                  |
| **Edit Profile**      | `UserGear`               | **Rotate**          | `Blue` tint. Gear spins 360° on hover.            | **Neutral**. Implies settings and maintenance.                       |
| **Suspend / Disable** | `UserCircleMinus`        | **Shake & Fade**    | `ghanaRed` glow. Icon shakes; `-` drops in.       | **Destructive / High**. Warns user they are deactivating an account. |
| **Verify / Hash ID**  | `Fingerprint`            | **Scan Line**       | `ghanaGreen`. A laser line sweeps down the print. | **Security / Medium**. Mimics biometric scanning.                    |
| **Mask / Unmask ID**  | `Eye` / `EyeSlash`       | **Slide / Morph**   | `Amber`. Slash slides across/away.                | **Privacy / Medium**. Signals data visibility toggling.              |
| **Switch Role**       | `ArrowsCounterClockwise` | **Continuous Spin** | `ghanaGold`. Spin speeds up on hover.             | **System State**. Shows the app is adapting to a new context.        |
| **View Logs**         | `ListMagnifyingGlass`    | **Magnify Scale**   | `Blue`. Glass scales up slightly.                 | **Informational**. Subtle invitation to inspect data.                |
| **Export Logs**       | `FileArrowDown`          | **Drop Bounce**     | `ghanaGreen`. Arrow bounces downward.             | **Constructive**. Implies saving data locally.                       |

---

### 📦 2. Acquisitions Module

_Focus: Financial Tracking, Vendor Relations, and Ordering_

| Entity / Action         | Phosphor Icon    | Animation Style     | Hover State & Color                           | Severity & UX Context                                              |
| :---------------------- | :--------------- | :------------------ | :-------------------------------------------- | :----------------------------------------------------------------- |
| **Add Vendor**          | `Storefront`     | **Awning Drop**     | `ghanaGold`. Awning drops down.               | **Constructive**. Welcoming new partners.                          |
| **Suspend Vendor**      | `Prohibit`       | **Shake & Flash**   | `ghanaRed`. Icon shakes and flashes red.      | **Destructive / High**. Blocks financial relationships.            |
| **Verify Business Reg** | `SealCheck`      | **Stamp Down**      | `ghanaGreen`. Checkmark stamps into the seal. | **Security / Medium**. Implies official validation.                |
| **Create Order**        | `FilePlus`       | **Fold Open**       | `Blue`. Paper folds open, `+` draws.          | **Constructive**. Starting a new workflow.                         |
| **Place / Submit**      | `PaperPlaneTilt` | **Fly Off**         | `ghanaGold`. Plane slides up and right.       | **Action / Medium**. Committing to a financial action.             |
| **Receive Shipment**    | `Package`        | **Unfold / Bounce** | `ghanaGreen`. Box lid lifts slightly.         | **Constructive**. Physical goods arriving.                         |
| **Track Budget**        | `Wallet`         | **Coin Drop**       | `Amber` (if <20% left). Coin drops in.        | **Financial / Contextual**. Color shifts based on budget severity. |
| **Withdraw Book**       | `Archive`        | **Drop & Fade**     | `Gray` → `Red`. Box drops, fades out.         | **Destructive / Medium**. Removing from active circulation.        |

---

### 🔍 3. Processing Module

_Focus: Physical Condition, Climate Risks, and Routing_

| Entity / Action       | Phosphor Icon             | Animation Style    | Hover State & Color                              | Severity & UX Context                                         |
| :-------------------- | :------------------------ | :----------------- | :----------------------------------------------- | :------------------------------------------------------------ |
| **Inspect Condition** | `SlidersHorizontal`       | **Sliders Move**   | `Blue`. Sliders animate to random positions.     | **Interactive**. Invites the user to adjust physical ratings. |
| **Assess Mold Risk**  | `Drop` / `Warning`        | **Ripple / Pulse** | `Amber` / `Red`. Drop ripples or Warning pulses. | **Warning / High**. Critical Ghana climate adaptation alert.  |
| **Assign Curriculum** | `Tag`                     | **Swing**          | `ghanaGold`. Tag swings like a pendulum.         | **Neutral**. Categorization action.                           |
| **Generate Barcode**  | `Barcode`                 | **Laser Sweep**    | `ghanaGreen`. Laser line sweeps across bars.     | **System / Medium**. Mimics physical barcode generation.      |
| **Route to Section**  | `ArrowLineRight`          | **Draw Path**      | `Blue`. Arrow draws its path to the right.       | **Action / Low**. Directing physical flow.                    |
| **Approve / Reject**  | `CheckCircle` / `XCircle` | **Draw / Stamp**   | `Green` (Check draws) / `Red` (X stamps).        | **Decision / High**. Finalizing the quality control chain.    |
| **Rate Durability**   | `ShieldCheck`             | **Shield Pulse**   | `ghanaGreen`. Shield pulses with a checkmark.    | **Security / Medium**. Protecting Extension Services books.   |
| **Create Badge**      | `Medal`                   | **Gleam / Shine**  | `ghanaGold`. Gleam sweeps across the medal.      | **Reward / Low**. Celebrating patron achievements.            |

---

### 🚚 4. Distribution Module

_Focus: Logistics, Rural Delivery, and Safety_

| Entity / Action       | Phosphor Icon      | Animation Style    | Hover State & Color                           | Severity & UX Context                                                 |
| :-------------------- | :----------------- | :----------------- | :-------------------------------------------- | :-------------------------------------------------------------------- |
| **Create Dispatch**   | `Truck`            | **Bounce / Drive** | `Blue`. Truck bounces on its suspension.      | **Action / Low**. Preparing for physical transit.                     |
| **Mark Delivered**    | `CheckFat`         | **Stamp**          | `ghanaGreen`. Stamps down with a green flash. | **Success / High**. Confirming physical receipt.                      |
| **Enable Rural Mode** | `MapPinArea`       | **Radar Pulse**    | `Amber`. Radar pulse emits from the pin.      | **Contextual / Medium**. Signals GPS-disabled, community-led routing. |
| **Generate PDF**      | `FilePdf`          | **Fold**           | `Red`. Paper folds, PDF icon appears.         | **System / Low**. Document generation.                                |
| **Notify Leader**     | `ChatTeardropText` | **Pop / Bounce**   | `ghanaGreen`. Bubble pops up.                 | **Communication / Low**. SMS/Dagbani template trigger.                |

---

### 👧 5. Patron Intelligence & Library Sections

_Focus: Degradation Tracking, Batch Promotion, and Patron Behavior_

| Entity / Action       | Phosphor Icon    | Animation Style    | Hover State & Color                     | Severity & UX Context                                             |
| :-------------------- | :--------------- | :----------------- | :-------------------------------------- | :---------------------------------------------------------------- |
| **Issue Book**        | `BookArrowRight` | **Slide Out**      | `Blue`. Book slides out to the right.   | **Action / Medium**. Circulation workflow.                        |
| **Return Book**       | `BookArrowLeft`  | **Slide In**       | `ghanaGreen`. Book slides back in.      | **Action / Medium**. Circulation workflow.                        |
| **Block / Override**  | `ShieldWarning`  | **Shake / Flash**  | `ghanaRed`. Shield shakes, flashes red. | **Destructive / Critical**. Blocking a patron due to degradation. |
| **View "Teleporter"** | `Lightning`      | **Flash / Zap**    | `Purple` / `Amber`. Lightning flashes.  | **Anomaly / High**. Flagging suspicious pristine returns.         |
| **Promote Batch**     | `ArrowSquareUp`  | **Slide Up**       | `ghanaGreen`. Arrow slides up smoothly. | **Success / Medium**. GES academic calendar progression.          |
| **Expire Batch**      | `ClockCountdown` | **Tick / Fade**    | `Red`. Ticks down, fades to red.        | **Warning / High**. Academic year hard stop (Aug 31).             |
| **Track Attendance**  | `CheckSquare`    | **Check Draw**     | `ghanaGreen`. Check draws itself.       | **Success / Low**. Reading program engagement.                    |
| **Appraise Patron**   | `Star`           | **Fill / Sparkle** | `ghanaGold`. Star fills and sparkles.   | **Reward / Low**. Staff appraisal and notes.                      |

---

### 🌍 6. Extension Services Department

_Focus: Bulk Allocation, Rotation Cycles, and Mobile Outreach_

| Entity / Action         | Phosphor Icon | Animation Style     | Hover State & Color                        | Severity & UX Context                                      |
| :---------------------- | :------------ | :------------------ | :----------------------------------------- | :--------------------------------------------------------- |
| **Create Bulk Request** | `FileArrowUp` | **Slide Up**        | `Blue`. File slides up.                    | **Action / Medium**. Requesting from Lending.              |
| **Fulfill Request**     | `Handshake`   | **Clasp / Squeeze** | `ghanaGreen`. Hands clasp together.        | **Success / High**. Cross-department boundary handshake.   |
| **Reject Request**      | `XCircle`     | **Shake**           | `ghanaRed`. Shakes horizontally.           | **Destructive / High**. Denying bulk allocation.           |
| **Generate QR Tag**     | `QrCode`      | **Grid Fill**       | `Blue`. Grid fills in sequentially.        | **System / Low**. Privacy-first learner ID generation.     |
| **Scan Checkout**       | `Scan`        | **Laser Sweep**     | `Blue`. Laser sweeps down.                 | **System / Medium**. Android app offline scanning.         |
| **Plan Route**          | `MapTrifold`  | **Unfold**          | `Blue`. Map unfolds.                       | **System / Low**. Tamale-Bolgatanga corridor planning.     |
| **Trigger Safety**      | `Siren`       | **Flash / Rotate**  | `Red` / `Blue`. Siren flashes and rotates. | **Critical / High**. Corridor safety protocol (rain/road). |
| **Assemble Set**        | `Stack`       | **Drop Stack**      | `Blue`. Layers drop in one by one.         | **Action / Low**. Grouping books for rotation.             |

---

### 🛡️ 7. System Infrastructure & Data Ops

_Focus: Offline-First Resilience, Backups, and Sync_

| Entity / Action       | Phosphor Icon          | Animation Style     | Hover State & Color                             | Severity & UX Context                                 |
| :-------------------- | :--------------------- | :------------------ | :---------------------------------------------- | :---------------------------------------------------- |
| **Trigger Backup**    | `CloudArrowUp`         | **Float Up**        | `Blue`. Cloud floats, arrow uploads.            | **System / Medium**. Data safety.                     |
| **Restore Backup**    | `CloudArrowDown`       | **Float Down**      | `ghanaGreen`. Cloud floats, arrow downloads.    | **System / Medium**. Disaster recovery.               |
| **Verify Integrity**  | `ShieldCheck`          | **Scan / Pulse**    | `ghanaGreen`. Shield pulses.                    | **Security / High**. SHA-256 checksum audit.          |
| **Sync Status**       | `ArrowsClockwise`      | **Continuous Spin** | `Blue`. Spins continuously; speeds up on hover. | **System / Neutral**. PouchDB ↔ CouchDB replication.  |
| **Resolve Conflict**  | `GitMerge` / `Warning` | **Pulse / Shake**   | `Amber` / `Red`. Branches merge or shakes.      | **Critical / High**. Manual sync conflict resolution. |
| **Switch Country**    | `Globe`                | **Rotate**          | `Blue`. Globe rotates on its axis.              | **System / Low**. Changing jurisdiction policy.       |
| **Update Curriculum** | `BookBookmark`         | **Flag Wave**       | `ghanaGold`. Bookmark waves.                    | **System / Low**. MoE/GES tag updates.                |

---

### 💻 How to Prompt Your AI Assistant in VS Code

When you are ready to build these components, you can use this **exact prompt template** in your AI Chat (e.g., TONGYI Lingma or Continue) to generate the React/Tailwind code with the animations baked in:

> **"Create a React component for the 'Suspend Vendor' button using Tailwind CSS and Phosphor Icons (`Prohibit`).**
> **Animation Rules:**
>
> 1. Default state: Gray-500 stroke.
> 2. Hover state: The icon should shake horizontally (CSS keyframes) and change to `ghanaRed` (`#CE1126`).
> 3. Use `group-hover` classes.
> 4. Add a subtle red background fade (`bg-red-50`) on the button container on hover.
> 5. Ensure `prefers-reduced-motion` is respected by disabling the shake animation if the user has motion sensitivity turned on.
>    **Context:** This is a destructive action, so the hover state must clearly warn the user before they click."

### ⚙️ CSS Implementation Tip for the "Shake" (Destructive Actions)

Add this to your global `index.css` or `tailwind.css` to enable the destructive shake animation across your app:

```css
@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  20%,
  60% {
    transform: translateX(-2px);
  }
  40%,
  80% {
    transform: translateX(2px);
  }
}

.icon-shake:hover {
  animation: shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

/* Respect user accessibility settings */
@media (prefers-reduced-motion: reduce) {
  .icon-shake:hover {
    animation: none;
    transform: scale(1.1); /* Fallback to simple scale */
  }
}
```

This system ensures that your LMS doesn't just _look_ good—it _feels_ responsive, culturally aware, and perfectly aligned with the severity of library operations in Ghana!
