# Catalog content brief

What to produce for the online catalog. Every image must be **original** (made by our designers or generated
by us with an AI tool whose terms allow commercial use) or **commercially licensed** for use inside an app.
Never copy, trace or img2img another app's drawings.

## Style rules (all images)

- Black line art on a pure white background. No color fill, no gray shading on beginner items.
- Single subject, centered, filling about 80% of the frame, with nothing cut off at the edges.
- Clean, closed lines; stroke weight readable when the phone shows it at 30–50% opacity.
- Portrait 3:4 or square, at least 1500 px on the long side. PNG or JPG.
- No text, logos, watermarks, signatures, brand cars/characters, real celebrities or trademarked characters.
- File names describe the subject (`sleeping_cat.png`): they become the item name in the app.

Difficulty, used in the subject lists below:
- **Easy**: under 15 lines, big simple shapes.
- **Medium**: some detail.
- **Hard**: detailed with light hatching.

## Launch target: about 220 images in 16 categories

| Category (folder name) | Count | Mix | Subject ideas |
|---|--:|---|---|
| Easy Start | 20 | all easy | heart, star, smiley, cloud, balloon, leaf, moon, fish, house, cup, apple, flower, sun, umbrella, kite |
| Animals | 25 | easy/medium | cat, dog, puppy, bunny, fox, owl, elephant, lion, giraffe, horse, turtle, penguin, deer, panda, butterfly |
| Cute | 20 | easy | kawaii food with faces, chibi animals, baby dino, cloud with face, boba tea, cactus, mushroom house |
| Anime | 20 | medium/hard | original girl/boy portraits, eyes study, hairstyles, school uniform, chibi poses (no existing characters) |
| People | 20 | medium/hard | portraits, hands, poses, couple, grandparent, child reading, dancer, musician |
| Anatomy | 12 | medium/hard | eyes, nose, lips, ears, hands, feet, face proportions, skull, figure poses |
| Nature | 18 | easy/medium | trees, mountains, waves, flowers, roses, sunflower, leaves, landscape, moon and stars |
| Food | 12 | easy | cupcake, donut, pizza slice, ice cream, burger, fruit bowl, sushi, coffee cup |
| Cars & Vehicles | 12 | medium | generic sports car, classic car, truck, bike, motorbike, plane, train, ship (no brand designs) |
| Architecture | 10 | medium/hard | cottage, castle, lighthouse, temple, bridge, city skyline, windmill |
| Objects | 12 | easy/medium | guitar, camera, shoe, lamp, book stack, teapot, clock, headphones |
| Aesthetic | 12 | medium | moon phases, butterflies with flowers, line-art faces, celestial, botanical frames |
| One-line | 10 | easy | single continuous line faces, cat, hands, flower |
| Mandala & Patterns | 8 | hard | mandalas, zentangle, geometric |
| 3D Shapes | 6 | medium | cube, sphere, cylinder, cone, pyramid, 3D letters with shading guides |
| Seasonal | 3 | easy/medium | rotate monthly (Halloween, Christmas, Valentine's, Diwali, Eid) |

Order of chips in the app: put this in `content_src/categories.txt`:

```
Easy Start
Animals
Cute
Anime
People
Nature
Food
Cars & Vehicles
Aesthetic
One-line
Anatomy
Architecture
Objects
Mandala & Patterns
3D Shapes
Seasonal
```

Mark about 25% as `is_premium` once a paywall exists. Keep all of Easy Start free.

## AI prompt template

```
clean black line art drawing of {SUBJECT}, {DIFFICULTY_STYLE}, centered, full subject visible,
pure white background, coloring book style, no shading, no color, no text, no watermark
```

- easy: `very simple, thick outlines, minimal details, for beginners`
- medium: `moderate detail, smooth even outlines`
- hard: `detailed, fine lines, light hatching`

Review every generated image: fix broken lines and extra fingers, and reject anything that resembles an existing
character, logo or another app's artwork.

## After launch

Add about 20–40 images a week, plus a seasonal category before each holiday. Each push shows up in the
app without an update.
