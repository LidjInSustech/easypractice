import pygame as pg
import util
import skills.skills as skills

class Page(util.Rolling_Box):
    def __init__(self):
        dictionary = skills.dictionary
        skill_names = list(dictionary.keys())
        self.skill_names = skill_names
        self.load_description()
        self.load_player()
        rect = pg.display.get_surface().get_rect()
        self.plane = infomation_plane(pg.Rect(rect.width*0.4, rect.height*0.05, rect.width*0.5, rect.height*0.9))
        rect.width = rect.width//3
        button_rect = pg.Rect(0, 0, rect.width, rect.height*0.18)
        super().__init__(rect, button_rect, [self.description.get(i, {'name':i})['name'] for i in skill_names], util.load_image('basic/loading_page.png'))

    def start(self):
        rect = pg.display.get_surface().get_rect()
        message = super().start()
        while message != -1:
            weapon = util.Button_Box(pg.Rect(rect.w/3, rect.h/3, rect.w/3, rect.h/3), ['primary weapon', 'sub weapon'], self.picture)
            weapon = weapon.start()
            if weapon >= 0:
                index = util.Button_Box(pg.Rect(rect.w/3, 0, rect.w/3, rect.h), ['1', '2', '3', '4', '5', '6'], self.picture)
                index = index.start()
                if index >= 0:
                    self.player['primary weapon' if weapon == 0 else 'sub weapon']['skills'][index] = self.skill_names[self.curser]
                    self.save_player()
            message = super().start()

    def draw(self):
        super().draw()
        if self.skill_names[self.curser] in self.description:
            name = self.description[self.skill_names[self.curser]]['name']
            icon = pg.Surface((64, 64))
            desc = self.description[self.skill_names[self.curser]]['desc']
            playerinfo = self.get_player_info(self.player, self.skill_names[self.curser])
            self.plane.draw(name, icon, desc, playerinfo)
        pg.display.flip()

    def load_description(self):
        self.description = util.load_text('skills')

    def load_player(self):
        self.player = util.read_config('player.json')
        if len(self.player['primary weapon']['skills']) != 6:
            self.player['primary weapon']['skills'] = ['Skill'] * 6
        if len(self.player['sub weapon']['skills']) != 6:
            self.player['sub weapon']['skills'] = ['Skill'] * 6

    def save_player(self):
        util.write_config('player.json', self.player)

    def get_player_info(self, player, skill_name):
        text1 = []
        skills = player['primary weapon']['skills']
        for i in range(6):
            if skills[i] == skill_name:
                text1.append(str(i+1))
        text2 = []
        skills = player['sub weapon']['skills']
        for i in range(6):
            if skills[i] == skill_name:
                text2.append(str(i+1))
        text = ['']
        if len(text1) > 0:
            text.append(util.get_word('primary weapon') + ': ' + ', '.join(text1))
        if len(text2) > 0:
            text.append(util.get_word('sub weapon') + ': ' + ', '.join(text2))
        return text

class infomation_plane():
    def __init__(self, rect):
        self.rect = rect
        self.image = pg.Surface(rect.size, pg.SRCALPHA)
        self.image.fill((255,255,255,128))
        self.label_image = util.load_image('basic/label.png', (rect.width, rect.height*0.18))
        self.font = util.get_font(32)
        self.iconlen = min(self.rect.width, self.rect.height*0.3)

    def draw(self, name, icon, desc, playerinfo):
        image = self.image.copy()
        iconlen = self.iconlen
        icon = pg.transform.scale(icon, (iconlen, iconlen))
        image.blit(icon, (self.rect.width-iconlen, 0))

        image.blit(self.label_image, (0, iconlen))

        font = self.font
        font_rect = font.get_rect(name)
        font_rect.center = (self.rect.width*0.5, iconlen + self.rect.height*0.09)
        font.render_to(image, font_rect, name, fgcolor=(251,254,110))
        
        lines = self.split_into(desc) + playerinfo
        for i in range(len(lines)):
            self.render_line(lines[i], i, image)
        
        pg.display.get_surface().blit(image, self.rect)

    def render_line(self, text, line, image):
        start = self.iconlen + self.rect.height*0.18 + line*self.font.get_sized_height()
        self.font.render_to(image, (0, start), text, fgcolor=(251,254,110))

    def split_into(self, text, length = 12):
        if len(text) <= length:
            return [text]
        else:
            return [text[:length]] + self.split_into(text[length:], length)
