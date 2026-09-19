# 6. Visual assets

Icons, avatars, illustrations, social preview images. Where an external image
tool earns its place, where it actively hurts, and how to keep a generated set
from looking assembled.

## First: what you should *not* generate

| Do not generate | Use instead |
|---|---|
| **UI icons** | A real icon library — Lucide, Phosphor, Heroicons |
| **A logo with text in it** | A designer, or a type-based wordmark you set yourself |
| **Anyone's likeness** | Commissioned photography, or a licensed stock portrait |
| **Certification badges, awards, review stars** | Nothing. Fabricating these is fraud, not design |
| **Another company's brand marks** | Their official press kit, under their terms |

The icon row is the one people get wrong most. Generated icons are inconsistent
across a set — stroke weight drifts, optical size drifts, metaphor style drifts
— and **mixed icon styles are one of the loudest machine-made tells**
([chapter 5](05-not-looking-ai-made.md)). A real icon library is free, vector,
consistent by construction, and takes one minute to install.

Generate what a library cannot give you: **illustration, avatars, textures,
social preview art, section backgrounds.**

## The consistency problem

Generate eight images in eight prompts and you get eight styles. The fix is a
locked prompt template, where only one slot changes:

```
Style anchor (identical in every prompt):
  flat vector illustration · two-tone · palette #<accent> and #<surface>
  · rounded geometry · no gradients · no text · no shadows
  · consistent 4px visual stroke weight · plain <surface> background
  · square composition, subject centred with even margin

Subject (the only line that changes):
  A <subject>, viewed from <angle>.
```

Four rules that do most of the work:

1. **Lock the palette to your tokens.** Name the hex values in the prompt. This
   is what stops the purple default from arriving through the back door.
2. **Forbid text inside images.** Generated lettering is unreliable, and text in
   an image is invisible to search and to screen readers anyway.
3. **Generate the whole set in one session**, in one batch. A set generated
   across two days will not match.
4. **Name the negative space.** "Plain background, subject centred, even margin"
   is what makes eight images sit on a page as a set.

## The revision loop

Where the quality actually comes from. Generation is the cheap part.

```
1  Generate the full set with the locked template
2  Put them side by side and compare — as a set, never one at a time
3  Name what is off, specifically, per image
4  Regenerate only the outliers, same template, adjusted subject line
5  Repeat until the set is coherent
6  Then, and only then, optimise and ship
```

Step 2 is the whole thing. An image judged alone always looks fine; the same
image next to its seven siblings shows its drift immediately.

Useful critique vocabulary for step 3 — specific, not "make it better":

- "Stroke weight is heavier than the others — match image 3"
- "This one has a perspective view, the rest are front-on"
- "Background is off-white, the set is pure `surface`"
- "Subject fills the frame; the others have a margin"
- "This introduced a third colour"

### Where Claude fits in this loop

Not as the generator — as the **critic and the bookkeeper**:

- Compare the set against the style anchor and list the outliers
- Keep the prompt template and the per-image subject lines in the repo, so the
  set is reproducible in six months
- Handle everything after step 6 — optimisation, naming, alt text, markup

## Buttons and components

A related trap: generating a **picture** of a button. Buttons are code — they
need hover, focus, active, disabled and loading states, and an image has none
of them.

What an image tool is genuinely useful for here is **exploration**: generate a
few visual directions for a component, react to them, and then have the
developer agent build the chosen one properly in CSS with all its states.

> Image for deciding. Code for shipping.

## After generation

Everything below is mechanical, and belongs to Claude and to scripts:

| Step | What good looks like |
|---|---|
| **Format** | AVIF or WebP with a fallback. PNG only for genuine transparency needs |
| **Size** | Exported at the largest rendered size, then responsive `srcset` |
| **Weight** | Under ~150 KB for a hero, under ~40 KB for an inline illustration |
| **Dimensions** | Width and height always set — missing dimensions cause layout shift |
| **Alt text** | Describes the content and its purpose. Decorative images get `alt=""`, not a caption |
| **OG image** | 1200×630, readable at thumbnail size, no small text |
| **Naming** | `service-lock-repair.avif`, not `image_final_v3.png` |

The `seo-images` skill audits all of that; `seo-image-gen` plans what is missing
before you generate anything.

## Keeping it reproducible

Commit the recipe next to the output:

```
public/images/
  illustrations/
    RECIPE.md          the style anchor, verbatim
    lock-repair.avif
    lock-repair.prompt.txt
    key-cutting.avif
    key-cutting.prompt.txt
```

Six months later, when one image needs replacing, the set can be matched instead
of restarted. This is the difference between a set and a pile.
