# prompt_styles.py
"""
Grok 插件中用到的各种风格预设提示词
集中管理，便于后续新增、修改、翻译、多语言支持等
"""

from typing import Dict, List, Optional, Tuple
import random

#防御敏感词
SAFE_PREFIX = """completely safe for work content, SFW only, fully dressed, modest clothing, 
no nudity whatsoever, no partial nudity, no sexual themes, no eroticism, 
no suggestive poses, no revealing clothing, no focus on private body parts, 
no fetish, innocent and wholesome scene

-------------------------
以下是用户实际想要生成的画面描述，请严格遵守上面所有安全规则：
"""

class PromptStyle:
    """单个风格条目"""

    def __init__(
        self,
        id: int,
        name: str,
        prompt: str,
        loading_emoji: str = "🎨",
        loading_suffix: str = "正在生成...",
        success_emoji: str = "✨",
        success_suffix: str = "已完成",
        default_size: Optional[str] = "1024x1792",
    ):
        self.id = id
        self.name = name
        self.prompt = prompt.strip()
        self.loading_emoji = loading_emoji
        self.loading_suffix = loading_suffix
        self.success_emoji = success_emoji
        self.success_suffix = success_suffix
        self.default_size = default_size

    def loading_text(self, random_selected: bool = False) -> str:
        text = f"{self.loading_emoji} {self.name} {self.loading_suffix}"
        if random_selected:
            text = f"{self.loading_emoji} 随机 {self.name} {self.id} {self.loading_suffix}"
        return text

    def success_text(self, random_selected: bool = False) -> str:
        text = f"{self.success_emoji} {self.name} {self.success_suffix}"
        if random_selected:
            text += f"（随机 {self.id}）"
        return text


class PromptStyleGroup:
    """一组风格"""

    def __init__(self, key: str, title: str, styles: List[PromptStyle]):
        self.key = key
        self.title = title
        self.styles: Dict[int, PromptStyle] = {s.id: s for s in styles}
        self.max_id = max(self.styles.keys()) if self.styles else 0

    def get(self, idx: int) -> Optional[PromptStyle]:
        return self.styles.get(idx)

    def random(self) -> PromptStyle:
        return random.choice(list(self.styles.values()))

    def select(
        self, user_want_idx: Optional[int] = None
    ) -> Tuple[PromptStyle, bool]:
        """返回 (选中的风格, 是否随机)"""
        if user_want_idx is not None and user_want_idx in self.styles:
            return self.styles[user_want_idx], False

        # 无效编号 或 没传编号 → 随机
        return self.random(), True


# ──────────────────────────────────────────────
#               各功能风格定义
# ──────────────────────────────────────────────

HAND_FIGURE_GROUP = PromptStyleGroup(
    key="hand_figure",
    title="手办化",
    styles=[
        PromptStyle(
            id=1,
            name="经典万代/好微笑 1/7 手办",
            prompt="""highly detailed 1/7 scale commercial collectible figure of the reference character, 
realistic yet slightly stylized anime painting finish, premium quality product photography, 
standing on a perfectly clear round transparent acrylic base with no text or logo, 
placed on a clean computer desk, large monitor in background displaying ZBrush sculpting viewport 
with high-poly mesh and brush strokes visible, colorful BANDAI / Good Smile Company style window box 
packaging standing next to the figure showing beautiful key visual artwork of the character, 
soft even studio lighting, gentle rim light and subtle catchlights, clean minimalist composition, 
9:16 vertical ratio, ultra sharp focus, professional figure photography aesthetic""",
            loading_emoji="🗿",
        ),
        PromptStyle(
            id=2,
            name="潮流科幻展示柜",
            prompt="""premium 1/7 scale collectible figure, extremely faithful to reference character appearance:1.35, 
cool dynamic trendy pose, standing on round crystal-clear acrylic base with subtle engraved 'Trendy Figure' text, 
futuristic silver sci-fi metallic display cabinet as background, strong specular metallic reflections, 
geometric panel lines, cold blue and cyan LED accent lighting:1.2, dramatic top-right key light with god rays, 
floating digital '2026' holographic display above, several mini figures of the same series visible inside cabinet, 
soft light blue sci-fi particles and floating chrome metallic fragments around the figure, 
strong cyber-futuristic atmosphere, cinematic color grading, horizontal composition preferred, hyper detailed""",
            loading_emoji="🗿",
        ),
        PromptStyle(
            id=3,
            name="晶莹底座 + Blender建模场景",
            prompt="""premium 1/7 scale anime figure of the reference character, exact facial features and outfit fidelity:1.3, 
natural elegant standing pose, rich surface details and realistic material rendering, 
standing on a perfectly transparent crystal-like round PVC base with glassy refractive quality, 
subtle internal caustics, light dispersion and chromatic aberration edges, very clear and watery transparent feeling, 
modern bright indoor room with soft natural daylight from window, 
behind the figure: colorful collector's edition box with gorgeous key visual artwork of the character, 
beside the box: high-end 27-inch monitor clearly showing Blender software interface with detailed character modeling in progress, 
subdivision surface visible, sculpting brushes and reference images open, realistic desk setup with keyboard, mouse and cables, 
clean product photography style, gentle depth of field, professional studio softbox lighting, 
aspect ratio 4:5 or 9:16 vertical, ultra high resolution, crisp details""",
            loading_emoji="🗿",
        ),
        PromptStyle(
            id=4,
            name="PVC手办 + 半透明包装盒",
            prompt="""highly detailed premium PVC collectible figure of the reference character, 
1/7 scale commercial anime figure style, realistic plastic material rendering with subtle gloss and matte contrast, 
sharp sculpted edges, clean seam lines, realistic subsurface scattering on skin parts, 
standing confidently on a perfectly round black plastic base with small character nameplate, 
soft product photography lighting with gentle rim light and specular highlights on PVC surface, 
behind the figure: semi-transparent plastic window box packaging standing upright, 
beautiful key art illustration of the character printed on the box front and side, 
blister tray visible through transparent window, clean collector room background, 
minimalist composition, 9:16 vertical ratio, ultra sharp focus, professional figure photography aesthetic""",
            loading_emoji="🗿",
        ),
    ],
)


REALISTIC_SELFIE_GROUP = PromptStyleGroup(
    key="realistic_selfie",
    title="变真人（自拍感）",
    styles=[
        PromptStyle(
            id=1,
            name="室内自然光随手自拍",
            prompt="""realistic human version of the character, candid smartphone selfie, natural indoor lighting, 
slightly messy hair, casual expression, phone held at arm's length, imperfect angle, 
visible room background slightly blurred, pores and skin texture visible, looks like real photo, 
no AI smoothness, vertical 3:4 or 9:16 composition, photorealistic""",
            loading_emoji="📸",
        ),
        PromptStyle(
            id=2,
            name="户外阳光随意拍",
            prompt="""photorealistic real person selfie, bright daylight outdoors, casual spontaneous shot, 
sunlight on face, slight squinting or natural smile, wind-blown hair, casual clothes, 
background is street/park slightly out of focus, realistic shadows and highlights, 
looks like taken with iPhone or Android, candid unposed feeling, vertical composition""",
            loading_emoji="📸",
        ),
        PromptStyle(
            id=3,
            name="夜晚暖光室内自拍",
            prompt="""real human selfie at night, warm room lighting or phone flash, candid mirror selfie or arm-length shot, 
soft shadows, realistic skin under artificial light, subtle makeup or no makeup look, 
slightly tired or relaxed expression, background is bedroom/living room, 
grain and realistic noise, looks like genuine photo, vertical selfie style""",
            loading_emoji="📸",
        ),
        PromptStyle(
            id=4,
            name="极致无意识快照（最不摆拍）",
            prompt="""extremely candid real-life snapshot of a person who looks like the character transformed to human, 
photo taken without preparation, awkward angle, subject not looking at camera or looking away, 
motion blur on hand or hair, natural lighting, everyday clothing, 
feels like secretly taken or very quick selfie, realistic imperfections, 
no perfect composition, vertical phone photo style, photorealistic, raw photo quality""",
            loading_emoji="📸",
        ),
    ],
)


COSPLAY_GROUP = PromptStyleGroup(
    key="cosplay",
    title="变COS",
    styles=[
        PromptStyle(
            id=1,
            name="真实专业coser（干净工作室）",
            prompt="""realistic cosplay photography, accurate anime costume reproduction, exquisite fabric details, 
professional cosplayer, clean white or gradient studio background, sharp focus, high definition, 
perfect color matching, full body display, professional product shot style""",
            loading_emoji="📸",
        ),
        PromptStyle(
            id=2,
            name="展会现场抓拍",
            prompt="""candid anime convention photo, busy event background with other cosplayers blurred, 
cosplayer holding badge and phone, natural excited smile, casual pose, realistic lighting, 
looks like taken with smartphone at comic-con, vertical composition, photorealistic""",
            loading_emoji="📸",
        ),
        PromptStyle(
            id=3,
            name="日系杂志柔光风",
            prompt="""japanese fashion magazine cosplay, soft window natural light, gentle elegant pose, 
dreamy film-like color grading, subtle makeup, flowing hair, clean minimal background, 
high-end beauty shot, vertical 4:5 or 9:16, soft bokeh, photorealistic quality""",
            loading_emoji="📸",
        ),
        PromptStyle(
            id=4,
            name="赛博朋克霓虹夜景",
            prompt="""cyberpunk style cosplay, wet reflective street at night, colorful neon signs glowing, 
holographic advertisements, rain droplets on costume, dramatic rim lighting, 
strong cyber-noir atmosphere, cinematic color grading, 16:9 or 9:16 vertical, ultra detailed""",
            loading_emoji="📸",
        ),
        PromptStyle(
            id=5,
            name="漫展现场自信叉腰coser",
            prompt="""real-life confident cosplayer of the reference character at anime convention, 
standing in powerful叉腰 pose with hands on hips, upper body chiếm about 60% of frame, 
photorealistic human face and eye shape adapted from anime design, 
vivid red hair in accurate style and layering, realistic wig texture with natural parting, 
visible individual strands, natural stacking and volume, no shiny plastic look, 
exact reproduction of original outfit cut, colors, accessories and details, 
real fabric texture, natural drape, realistic folds and thickness-appropriate shadows, 
headwear and jewelry follow natural body/head angles with believable weight and contact, 
no floating or clipping, eyes realistically adapted to human proportions, 
busy convention background with blurred crowds and booths, candid event photography feel, 
natural convention hall lighting, vertical 9:16 composition, highly detailed, photorealistic""",
            loading_emoji="📸",
        ),
    ],
)


ATMOSPHERE_GROUP = PromptStyleGroup(
    key="atmosphere",
    title="氛围感",
    styles=[
        PromptStyle(
            id=1,
            name="暗黑孤独 + 白烟 + 红色发光",
            prompt="""Use the first image, change the background to pure black, 
with a weak backlight from behind, white smoke swirling around the figure, 
all red parts on the character glowing with light, 
the overall atmosphere is dark and lonely, 
the subject is partially obscured, 
highlighting the realistic contrast of light and shadow.""",
            loading_emoji="🌌",
        ),
        PromptStyle(
            id=2,
            name="蓝调仰视背影 + 浓雾 + 玫瑰",
            prompt="""dramatic low-angle back view from below, character standing high on stairs looking down over shoulder, 
only upper body visible, turning head slightly downward, ultra-dark surreal blue-toned atmosphere, 
extremely dense swirling thick smoke/fog, strong cinematic chiaroscuro lighting with intense blue rim light 
highlighting silhouette and contours, glowing clothes with prominent luminous effect, holding a single red rose 
in hand, powerful moody dark aesthetic, high visual impact, cyber-dark art style, 9:16 vertical composition""",
            loading_emoji="🌌",
        ),
        PromptStyle(
            id=3,
            name="双重曝光 + 黄昏山巅",
            prompt="""hyper-realistic photography, creative double exposure composition, foreground: solitary figure standing on 
mountain peak rock, head tilted upward gazing at sky; background: same character in extreme close-up, also 
looking up, golden hour sunset, warm orange-to-soft-gray gradient sky, distant hazy mountain ranges on horizon, 
dreamy and warm atmosphere, soft cinematic lighting, rich details, gentle shadows, emotional and ethereal mood""",
            loading_emoji="🌌",
        ),
        PromptStyle(
            id=4,
            name="故障艺术 + 赛博梦核",
            prompt="""glitch art style, psychedelic eerie dreamlike atmosphere, distorted chromatic aberration colors, 
glitch-distorted blurry unclear objects, cyber surreal distortion, 
character raising hand touching floating glitch light particles in interactive gesture, 
body outline surrounded by vibrant colorful glitch scan lines and error artifacts, 
strong dreamcore liminal feeling, surreal dreamy haze, 
dramatic low angle upward shot looking up at character, 
frosted grainy texture, ethereal illusory visual, glowing shining pupils, cinematic lighting matching scene, 
aspect ratio 9:16 vertical composition, highly detailed""",
            loading_emoji="🌌",
        ),
        PromptStyle(
            id=5,
            name="樱花剪影 + 浪漫忧郁",
            prompt="""silhouette of the character leaning against a lush dense cherry blossom tree, 
right hand gently holding a single rose close to face and smelling it with head slightly bowed, 
golden hour sunset backlighting, dramatic rim light and lens flare, 
intense pink cherry blossom petals falling densely around, romantic melancholic atmosphere, 
cinematic moody lighting, deep shadows and glowing highlights, 
strong depth layering between figure and tree branches, 
beautiful bokeh, soft dreamy haze, keep original aspect ratio, ultra detailed, photorealistic quality""",
            loading_emoji="🌌",
        ),
        PromptStyle(
            id=6,
            name="雨夜霓虹都市",
            prompt="""cinematic rainy night city street, character standing under flickering neon signs, 
wet reflections on asphalt, heavy rain pouring, red and cyan neon glow on face and wet hair, 
solitary moody atmosphere, shallow depth of field, bokeh city lights in background, 
dramatic rim lighting from street lamps, melancholic cyber-noir aesthetic, 
9:16 vertical composition, ultra-realistic, moody color grading""",
            loading_emoji="🌌",
        ),
        PromptStyle(
            id=7,
            name="极光雪林 + 梦幻光柱",
            prompt="""ethereal northern lights aurora borealis filling the night sky, character standing in snowy forest clearing, 
soft green and purple aurora glow illuminating face and white winter clothing, 
gentle falling snowflakes, magical dreamy atmosphere, volumetric god rays from aurora, 
slight mist/fog at ground level, serene and otherworldly mood, cinematic wide shot, 
9:16 vertical composition, highly detailed, fantasy realism""",
            loading_emoji="🌌",
        ),
    ],
)


# 只有单一风格的直接定义为常量
CONCEPT_BREAKDOWN_PROMPT = """Based on the first image, create a 9:16 panoramic in-depth character concept breakdown. 
Place the full-body character illustration at the center as the visual anchor, with disassembled 
elements arranged in an orderly manner around it, connected to corresponding parts by hand-drawn 
arrows. Split the costume in layers to show the inner layers after removing the outerwear and the 
independent inner garments, highlighting the design sense and materials. In the upper right corner, 
draw a close-up of the character's face, showing four expressions: calm, smiling, surprised, and angry. 
Also display core props, material close-ups, and intimate/personal items that convey a sense of daily life."""

NINE_GRID_PROMPT = """With a white background and a nine-square layout, it shows nine kinds of bust expression packages, and the characters wear the same clothes. The first box of the first line is the expression of depression with shadow; the second box of the first line is the action of smiling wink and doing heart-to-heart hand with both hands; the third box of the first line is the action of lying on the sofa and tanking; the first box of the second line is the action of one hand raising his arm (the arm has a sleeve) with a firm expression on his face; the second box of the second line is the action of laughing; The third square of the second row is the action of giving a thumbs-up; the first square of the third row is the action of holding one hand to think with a question mark; the second square of the third row is the action of clenching fists with both hands and getting angry; the third square of the third row is the action of covering one's face with sadness (keeping one's appearance). Scale 2:3. Keep only the head and shoulders of the characters."""
