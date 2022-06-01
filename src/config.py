from collections import namedtuple
from src.app.utils.enums.input_source import InputSource
from src.app.utils.enums.game_mode import GameMode
import os
import mediapipe as mp


HandLandmark = mp.solutions.hands.HandLandmark


def image_path(*parts):
    return os.path.join('assets', 'graphics', *parts)


WindowConfig = namedtuple('WindowConfig', [
    'TITLE',
    'WIDTH',
    'HEIGHT',
    'BACKGROUND_PATH'
])

GameConfig = namedtuple('GameConfig', [
    'FPS',
    'INPUT_SOURCE'
])

BladeConfig = namedtuple('BladeConfig', [
    'COLORS',
    'VISIBILITY_DURATION'
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

GameModeConfig = namedtuple('GameModeConfig', [
    'MODE',
    'LIVES',
    'DIFFICULTY'
    # TODO - add more params related to the game mode configuration
])

GameModesConfig = namedtuple('GameModesConfig', [
    'ZEN',
    'CLASSIC',
    'ARCADE',
    'MULTIPLAYER'
])

SpawnFrequencyConfig = namedtuple('SpawnFrequencyConfig', [
    'PLAIN_FRUIT',
    'BOMB'
])

MenuConfig = namedtuple('MenuConfig', [
    'PADDING',
    'BACK_BUTTON_IMAGE',
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


game_config = GameConfig(
    FPS=float('inf'),  # Unlimited
    INPUT_SOURCE=InputSource.HAND
)

window_config = WindowConfig(
    TITLE='Fruit ninja',
    WIDTH=800,
    HEIGHT=600,
    BACKGROUND_PATH=image_path('backgrounds', 'background.jpg')
)

blade_config = BladeConfig(
    COLORS=['white'],  # Todo - add gradient effect
    VISIBILITY_DURATION=.25
)

spawn_frequency = SpawnFrequencyConfig(
    PLAIN_FRUIT=5,
    BOMB=1
)

classic_mode_config = GameModeConfig(
    MODE=GameMode.CLASSIC,
    LIVES=6,
    DIFFICULTY=1
)

game_modes_config = GameModesConfig(
    ZEN=None,  # TODO
    CLASSIC=classic_mode_config,
    ARCADE=None,  # TODO
    MULTIPLAYER=None  # TODO
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

menu_config = MenuConfig(
    PADDING=20,
    BACK_BUTTON_IMAGE=image_path('gui', 'back-button.png'),
    ORIGINAL_INNER_IMAGE=image_path('items', 'fruits', 'watermelon.png'),
    ORIGINAL_OUTER_IMAGE=image_path('gui', 'circles', 'original.png'),
    MULTIPLAYER_INNER_IMAGE=image_path('items', 'fruits', 'peach.png'),
    MULTIPLAYER_OUTER_IMAGE=image_path('gui', 'circles', 'multiplayer.png'),
    QUIT_INNER_IMAGE=image_path('items', 'bombs', 'bomb.png'),
    QUIT_OUTER_IMAGE=image_path('gui', 'circles', 'quit.png'),
    CLASSIC_INNER_IMAGE=image_path('items', 'fruits', 'watermelon.png'),
    CLASSIC_OUTER_IMAGE=image_path('gui', 'circles', 'classic.png'),
    ARCADE_INNER_IMAGE=image_path('items', 'fruits', 'banana.png'),
    ARCADE_OUTER_IMAGE=image_path('gui', 'circles', 'arcade.png'),
    ZEN_INNER_IMAGE=image_path('items', 'fruits', 'apple.png'),
    ZEN_OUTER_IMAGE=image_path('gui', 'circles', 'zen.png'),
    CLASSIC_ATTACK_INNER_IMAGE=image_path('items', 'fruits', 'watermelon.png'),
    CLASSIC_ATTACK_OUTER_IMAGE=image_path('gui', 'circles', 'classic-attack.png'),
    ZEN_DUEL_INNER_IMAGE=image_path('items', 'fruits', 'apple.png'),
    ZEN_DUEL_OUTER_IMAGE=image_path('gui', 'circles', 'zen-duel.png')
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
