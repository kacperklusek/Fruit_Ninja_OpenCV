from collections import namedtuple
import mediapipe as mp
import os

from src.app.utils.enums import InputSource


HandLandmark = mp.solutions.hands.HandLandmark


def image_path(*parts):
    return os.path.join('assets', 'graphics', *parts)


WindowConfig = namedtuple('WindowConfig', [
    'TITLE',
    'WIDTH',
    'HEIGHT',
    'ICON_PATH',
    'BACKGROUND_PATH'
])

GameConfig = namedtuple('GameConfig', [
    'FPS',
    'INPUT_SOURCE',
    'FONT',
    'FONT_SIZE',
])

BladeConfig = namedtuple('BladeConfig', [
    'COLORS',
    'VISIBILITY_DURATION',
    'VALIDITY_DURATION_FOR_COLLISION'
])

HandInputConfig = namedtuple('HandInputConfig', [
    'MIN_DETECTION_CONFIDENCE',
    'MIN_TRACKING_CONFIDENCE'
])

FingerInputConfig = namedtuple('FingerInputConfig', [
    'FINGER_CODE',  # The number of the finger which will be tracked
    'MIN_DETECTION_CONFIDENCE',
    'MIN_TRACKING_CONFIDENCE'
])

MouseInputConfig = namedtuple('MouseInputConfig', [
    'REFRESH_FREQUENCY'  # Something like DPI in a mouse
])

SinglePlayerModeConfig = namedtuple('SinglePlayerModeConfig', [
    'BOARD_WIDTH',
    'BOARD_HEIGHT'
])

ClassicModeConfig = namedtuple('ClassicModeConfig', [
    'LIVES',  # TODO - rename to lives
    'BACKGROUND_PATH'
])

ZenModeConfig = namedtuple('ClassicModeConfig', [
    'BACKGROUND_PATH',
    'TIME'
])

SpawnFrequencyConfig = namedtuple('SpawnFrequencyConfig', [
    'PLAIN_FRUIT',
    'BOMB'
])

MenuConfig = namedtuple('MenuConfig', [
    'PADDING',
    'BACK_BUTTON_HOVER_DURATION',
    'HOVER_STOP_TOLERANCE',
    'BACK_BUTTON_IMAGE',
    'FRUIT_TEXT_IMAGE',
    'NINJA_TEXT_IMAGE',
    'INFO_TEXT_IMAGE',
    'NEW_TEXT_IMAGE',
    'BACKDROP_IMAGE',
    'ORIGINAL_INNER_IMAGE', 'ORIGINAL_OUTER_IMAGE',
    'MULTIPLAYER_INNER_IMAGE', 'MULTIPLAYER_OUTER_IMAGE',
    'QUIT_INNER_IMAGE', 'QUIT_OUTER_IMAGE',
    'CLASSIC_INNER_IMAGE', 'CLASSIC_OUTER_IMAGE',
    'ARCADE_INNER_IMAGE', 'ARCADE_OUTER_IMAGE',
    'ZEN_INNER_IMAGE', 'ZEN_OUTER_IMAGE',
    'CLASSIC_ATTACK_INNER_IMAGE', 'CLASSIC_ATTACK_OUTER_IMAGE',
    'ZEN_DUEL_INNER_IMAGE', 'ZEN_DUEL_OUTER_IMAGE'
])

SoundConfig = namedtuple('SoundConfig', [
    'BOOM', 'BOOM_VOLUME',
    'MENU', 'MENU_VOLUME',
    'OVER', 'OVER_VOLUME',
    'SPLATTER', 'SPLATTER_VOLUME',
    'START', 'START_VOLUME',
    'THROW', 'THROW_VOLUME'
])

HealthBarConfig = namedtuple('HealthBarConfig', [
    'GET_HEALTH_ICON',
    'GET_FAILED_HEALTH_ICON',
    'HEALTHS_COUNT'
])

EffectsConfig = namedtuple('EffectsConfig', [
    'DISPLAY_ITEM_TRAIL',
    'COMBO_FONT_SIZE'
])


game_config = GameConfig(
    FPS=float('inf'),  # Unlimited
    INPUT_SOURCE=InputSource.MOUSE,
    FONT=os.path.join('assets', 'fonts', 'go3v2.ttf'),
    FONT_SIZE=25
)

window_config = WindowConfig(
    TITLE='Fruit ninja',
    WIDTH=800,
    HEIGHT=600,
    ICON_PATH=image_path('icon.png'),
    BACKGROUND_PATH=image_path('backgrounds', 'background.jpg')
)

blade_config = BladeConfig(
    COLORS=['white'],  # Todo - add gradient effect
    VISIBILITY_DURATION=.25,
    VALIDITY_DURATION_FOR_COLLISION=.1
)

effects_config = EffectsConfig(
    DISPLAY_ITEM_TRAIL=True,
    COMBO_FONT_SIZE=20
)

spawn_frequency = SpawnFrequencyConfig(
    PLAIN_FRUIT=5,
    BOMB=1
)

single_player_mode_config = SinglePlayerModeConfig(
    BOARD_WIDTH=window_config.WIDTH,
    BOARD_HEIGHT=window_config.HEIGHT
)

classic_mode_config = ClassicModeConfig(
    BACKGROUND_PATH=image_path('backgrounds', 'background.jpg'),
    LIVES=6
)

zen_mode_config = ZenModeConfig(
    BACKGROUND_PATH=image_path('backgrounds', 'background.jpg'),
    TIME=90
)

mouse_input_config = MouseInputConfig(
    REFRESH_FREQUENCY=144
)

hand_input_config = HandInputConfig(
    MIN_TRACKING_CONFIDENCE=.5,
    MIN_DETECTION_CONFIDENCE=.5
)

finger_input_config = FingerInputConfig(
    FINGER_CODE=HandLandmark.INDEX_FINGER_TIP,
    MIN_TRACKING_CONFIDENCE=.5,
    MIN_DETECTION_CONFIDENCE=.5
)

health_bar_config = HealthBarConfig(
    GET_HEALTH_ICON=lambda i: image_path('gui', 'health', f'xf{i}.png'),
    GET_FAILED_HEALTH_ICON=lambda i: image_path('gui', 'health', f'x{i}.png'),
    HEALTHS_COUNT=3
)

menu_config = MenuConfig(
    PADDING=20,
    BACK_BUTTON_HOVER_DURATION=.75,
    HOVER_STOP_TOLERANCE=.2,
    FRUIT_TEXT_IMAGE=image_path('gui', 'logo-fruit.png'),
    NINJA_TEXT_IMAGE=image_path('gui', 'logo-ninja.png'),
    INFO_TEXT_IMAGE=image_path('gui', 'info-text.png'),
    NEW_TEXT_IMAGE=image_path('gui', 'new-text.png'),
    BACKDROP_IMAGE=image_path('gui', 'logo-backdrop.png'),
    BACK_BUTTON_IMAGE=image_path('gui', 'buttons', 'back.png'),
    ORIGINAL_INNER_IMAGE=image_path('items', 'fruits', 'watermelon.png'),
    ORIGINAL_OUTER_IMAGE=image_path('gui', 'buttons', 'original.png'),
    MULTIPLAYER_INNER_IMAGE=image_path('items', 'fruits', 'peach.png'),
    MULTIPLAYER_OUTER_IMAGE=image_path('gui', 'buttons', 'multiplayer.png'),
    QUIT_INNER_IMAGE=image_path('items', 'bombs', 'bomb.png'),
    QUIT_OUTER_IMAGE=image_path('gui', 'buttons', 'quit.png'),
    CLASSIC_INNER_IMAGE=image_path('items', 'fruits', 'watermelon.png'),
    CLASSIC_OUTER_IMAGE=image_path('gui', 'buttons', 'classic.png'),
    ARCADE_INNER_IMAGE=image_path('items', 'fruits', 'banana.png'),
    ARCADE_OUTER_IMAGE=image_path('gui', 'buttons', 'arcade.png'),
    ZEN_INNER_IMAGE=image_path('items', 'fruits', 'apple.png'),
    ZEN_OUTER_IMAGE=image_path('gui', 'buttons', 'zen.png'),
    CLASSIC_ATTACK_INNER_IMAGE=image_path('items', 'fruits', 'watermelon.png'),
    CLASSIC_ATTACK_OUTER_IMAGE=image_path('gui', 'buttons', 'classic-attack.png'),
    ZEN_DUEL_INNER_IMAGE=image_path('items', 'fruits', 'apple.png'),
    ZEN_DUEL_OUTER_IMAGE=image_path('gui', 'buttons', 'zen-duel.png')
)

general_volume = 0.1
lower_volume = 0.05
sound_config = SoundConfig(
    BOOM=os.path.join('assets', 'sounds', 'boom.mp3'), BOOM_VOLUME=1,
    MENU=os.path.join('assets', 'sounds', 'menu.mp3'), MENU_VOLUME=lower_volume,
    OVER=os.path.join('assets', 'sounds', 'over.mp3'), OVER_VOLUME=general_volume,
    SPLATTER=os.path.join('assets', 'sounds', 'splatter.mp3'), SPLATTER_VOLUME=lower_volume,
    START=os.path.join('assets', 'sounds', 'start.mp3'), START_VOLUME=general_volume,
    THROW=os.path.join('assets', 'sounds', 'throw.mp3'), THROW_VOLUME=lower_volume
)
