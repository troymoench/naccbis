# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from naccbis.query import PandasQuerySet


class Base(models.Model):
    """ Abstract base class for all models """
    objects = PandasQuerySet.as_manager()

    class Meta:
        abstract = True
        managed = False


class Guts(Base):
    season = models.IntegerField(primary_key=True)
    lg_r_pa = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bsr_bmult = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_hbp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_bb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_x1b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_x2b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_x3b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_hr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_sb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_cs = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_out = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_hbp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_bb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_x1b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_x2b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_x3b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_hr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    woba_scale = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rep_level = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'guts'


class PlayerId(Base):
    fname = models.CharField(primary_key=True, max_length=20)
    lname = models.CharField(max_length=20)
    team = models.CharField(max_length=5)
    season = models.IntegerField()
    player_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'player_id'
        unique_together = (('fname', 'lname', 'team', 'season'),)


class BattersOverall(Base):
    no = models.IntegerField(blank=True, null=True)
    fname = models.CharField(primary_key=True, max_length=20)
    lname = models.CharField(max_length=20)
    team = models.CharField(max_length=5)
    season = models.IntegerField()
    # fname = models.OneToOneField(PlayerId, related_name="+", on_delete=models.PROTECT)
    # lname = models.OneToOneField(PlayerId, related_name="+", on_delete=models.PROTECT)
    # team = models.OneToOneField(PlayerId, related_name="+", on_delete=models.PROTECT)
    # season = models.OneToOneField(PlayerId, related_name="+", on_delete=models.PROTECT)
    yr = models.CharField(max_length=2, blank=True, null=True)
    pos = models.CharField(max_length=15, blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bb_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    so_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    babip = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    iso = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ops = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'batters_overall'
        unique_together = (('fname', 'lname', 'team', 'season'),)


class DuplicateNames(Base):
    fname = models.CharField(primary_key=True, max_length=20)
    lname = models.CharField(max_length=20)
    team = models.CharField(max_length=5)
    season = models.IntegerField()
    id = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'duplicate_names'
        unique_together = (('fname', 'lname', 'team', 'season'),)


class GameLog(Base):
    game_num = models.IntegerField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    season = models.IntegerField()
    team = models.CharField(max_length=30)
    opponent = models.CharField(max_length=30, blank=True, null=True)
    result = models.CharField(max_length=1, blank=True, null=True)
    rs = models.IntegerField(blank=True, null=True)
    ra = models.IntegerField(blank=True, null=True)
    home = models.BooleanField(blank=True, null=True)
    conference = models.BooleanField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'game_log'
        unique_together = (('game_num', 'season', 'team'),)


class LeagueOffenseOverall(Base):
    season = models.IntegerField(primary_key=True)
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ops = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bb_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    so_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    iso = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    babip = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lg_r_pa = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bsr_bmult = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bsr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_hbp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_bb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_x1b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_x2b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_x3b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_hr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_sb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_cs = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lw_out = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_hbp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_bb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_x1b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_x2b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_x3b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ww_hr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    woba_scale = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    woba = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sbr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lg_wsb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wsb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wraa = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    off = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wrc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wrc_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    off_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rep_level = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'league_offense_overall'


class NameCorrections(Base):
    uc_fname = models.CharField(primary_key=True, max_length=20)
    uc_lname = models.CharField(max_length=20)
    uc_team = models.CharField(max_length=5)
    uc_season = models.IntegerField()
    c_fname = models.CharField(max_length=20)
    c_lname = models.CharField(max_length=20)
    type = models.CharField(max_length=1, blank=True, null=True)
    submitted = models.DateTimeField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'name_corrections'
        unique_together = (('uc_fname', 'uc_lname', 'uc_team', 'uc_season'),)


class Nicknames(Base):
    rid = models.IntegerField(blank=True, null=True)
    name = models.CharField(primary_key=True, max_length=20)
    nickname = models.CharField(max_length=20)

    class Meta(Base.Meta):
        db_table = 'nicknames'
        unique_together = (('name', 'nickname'),)


class RawBattersConference(Base):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(primary_key=True, max_length=35)
    team = models.CharField(max_length=5)
    season = models.IntegerField()
    yr = models.CharField(max_length=2, blank=True, null=True)
    pos = models.CharField(max_length=15, blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_batters_conference'
        unique_together = (('name', 'team', 'season'),)


class RawBattersConferenceInseason(Base):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(primary_key=True, max_length=35)
    team = models.CharField(max_length=5)
    season = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    yr = models.CharField(max_length=2, blank=True, null=True)
    pos = models.CharField(max_length=15, blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_batters_conference_inseason'
        unique_together = (('name', 'team', 'date'),)


class RawBattersOverall(Base):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(primary_key=True, max_length=35)
    team = models.CharField(max_length=5)
    season = models.IntegerField()
    yr = models.CharField(max_length=2, blank=True, null=True)
    pos = models.CharField(max_length=15, blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_batters_overall'
        unique_together = (('name', 'team', 'season'),)


class RawBattersOverallInseason(Base):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(primary_key=True, max_length=35)
    team = models.CharField(max_length=5)
    season = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    yr = models.CharField(max_length=2, blank=True, null=True)
    pos = models.CharField(max_length=15, blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_batters_overall_inseason'
        unique_together = (('name', 'team', 'date'),)


class RawGameLogFielding(Base):
    game_num = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=10)
    season = models.IntegerField()
    name = models.CharField(max_length=30)
    opponent = models.TextField(blank=True, null=True)
    score = models.CharField(max_length=10, blank=True, null=True)
    tc = models.IntegerField(blank=True, null=True)
    po = models.IntegerField(blank=True, null=True)
    a = models.IntegerField(blank=True, null=True)
    e = models.IntegerField(blank=True, null=True)
    fpct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dp = models.IntegerField(blank=True, null=True)
    sba = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    cspct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pb = models.IntegerField(blank=True, null=True)
    ci = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_game_log_fielding'
        unique_together = (('game_num', 'date', 'season', 'name'),)


class RawGameLogFieldingInseason(Base):
    game_num = models.IntegerField(primary_key=True)
    scrape_date = models.DateField()
    date = models.CharField(max_length=10, blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30)
    opponent = models.TextField(blank=True, null=True)
    score = models.CharField(max_length=10, blank=True, null=True)
    tc = models.IntegerField(blank=True, null=True)
    po = models.IntegerField(blank=True, null=True)
    a = models.IntegerField(blank=True, null=True)
    e = models.IntegerField(blank=True, null=True)
    fpct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dp = models.IntegerField(blank=True, null=True)
    sba = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    cspct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pb = models.IntegerField(blank=True, null=True)
    ci = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_game_log_fielding_inseason'
        unique_together = (('game_num', 'scrape_date', 'name'),)


class RawGameLogHitting(Base):
    game_num = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=10)
    season = models.IntegerField()
    name = models.CharField(max_length=30)
    opponent = models.TextField(blank=True, null=True)
    score = models.CharField(max_length=10, blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_game_log_hitting'
        unique_together = (('game_num', 'date', 'season', 'name'),)


class RawGameLogHittingInseason(Base):
    game_num = models.IntegerField(primary_key=True)
    scrape_date = models.DateField()
    date = models.CharField(max_length=10, blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30)
    opponent = models.TextField(blank=True, null=True)
    score = models.CharField(max_length=10, blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_game_log_hitting_inseason'
        unique_together = (('game_num', 'scrape_date', 'name'),)


class RawGameLogPitching(Base):
    game_num = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=10)
    season = models.IntegerField()
    name = models.CharField(max_length=30)
    opponent = models.TextField(blank=True, null=True)
    score = models.CharField(max_length=10, blank=True, null=True)
    w = models.IntegerField(blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    sv = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    era = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_game_log_pitching'
        unique_together = (('game_num', 'date', 'season', 'name'),)


class RawGameLogPitchingInseason(Base):
    game_num = models.IntegerField(primary_key=True)
    scrape_date = models.DateField()
    date = models.CharField(max_length=10, blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30)
    opponent = models.TextField(blank=True, null=True)
    score = models.CharField(max_length=10, blank=True, null=True)
    w = models.IntegerField(blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    sv = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    era = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_game_log_pitching_inseason'
        unique_together = (('game_num', 'scrape_date', 'name'),)


class RawPitchersConference(Base):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(primary_key=True, max_length=35)
    team = models.CharField(max_length=5)
    season = models.IntegerField()
    yr = models.CharField(max_length=2, blank=True, null=True)
    pos = models.CharField(max_length=15, blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    gs = models.IntegerField(blank=True, null=True)
    w = models.IntegerField(blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    sv = models.IntegerField(blank=True, null=True)
    cg = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    so_9 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    era = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_pitchers_conference'
        unique_together = (('name', 'team', 'season'),)


class RawPitchersConferenceInseason(Base):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(primary_key=True, max_length=35)
    team = models.CharField(max_length=5)
    season = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    yr = models.CharField(max_length=2, blank=True, null=True)
    pos = models.CharField(max_length=15, blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    gs = models.IntegerField(blank=True, null=True)
    w = models.IntegerField(blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    sv = models.IntegerField(blank=True, null=True)
    cg = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    so_9 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    era = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_pitchers_conference_inseason'
        unique_together = (('name', 'team', 'date'),)


class RawPitchersOverall(Base):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(primary_key=True, max_length=35)
    team = models.CharField(max_length=5)
    season = models.IntegerField()
    yr = models.CharField(max_length=2, blank=True, null=True)
    pos = models.CharField(max_length=15, blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    gs = models.IntegerField(blank=True, null=True)
    w = models.IntegerField(blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    sv = models.IntegerField(blank=True, null=True)
    cg = models.IntegerField(blank=True, null=True)
    sho = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    era = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wp = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    bk = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    so_9 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_pitchers_overall'
        unique_together = (('name', 'team', 'season'),)


class RawPitchersOverallInseason(Base):
    no = models.IntegerField(blank=True, null=True)
    name = models.CharField(primary_key=True, max_length=35)
    team = models.CharField(max_length=5)
    season = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    yr = models.CharField(max_length=2, blank=True, null=True)
    pos = models.CharField(max_length=15, blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    gs = models.IntegerField(blank=True, null=True)
    w = models.IntegerField(blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    sv = models.IntegerField(blank=True, null=True)
    cg = models.IntegerField(blank=True, null=True)
    sho = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    era = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wp = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    bk = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    so_9 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_pitchers_overall_inseason'
        unique_together = (('name', 'team', 'date'),)


class RawTeamFieldingConference(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    g = models.IntegerField(blank=True, null=True)
    tc = models.IntegerField(blank=True, null=True)
    po = models.IntegerField(blank=True, null=True)
    a = models.IntegerField(blank=True, null=True)
    e = models.IntegerField(blank=True, null=True)
    fpct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dp = models.IntegerField(blank=True, null=True)
    sba = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    cspct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pb = models.IntegerField(blank=True, null=True)
    ci = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_fielding_conference'
        unique_together = (('name', 'season'),)


class RawTeamFieldingConferenceInseason(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    g = models.IntegerField(blank=True, null=True)
    tc = models.IntegerField(blank=True, null=True)
    po = models.IntegerField(blank=True, null=True)
    a = models.IntegerField(blank=True, null=True)
    e = models.IntegerField(blank=True, null=True)
    fpct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dp = models.IntegerField(blank=True, null=True)
    sba = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    cspct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pb = models.IntegerField(blank=True, null=True)
    ci = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_fielding_conference_inseason'
        unique_together = (('name', 'date'),)


class RawTeamFieldingOverall(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    g = models.IntegerField(blank=True, null=True)
    tc = models.IntegerField(blank=True, null=True)
    po = models.IntegerField(blank=True, null=True)
    a = models.IntegerField(blank=True, null=True)
    e = models.IntegerField(blank=True, null=True)
    fpct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dp = models.IntegerField(blank=True, null=True)
    sba = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    cspct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pb = models.IntegerField(blank=True, null=True)
    ci = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_fielding_overall'
        unique_together = (('name', 'season'),)


class RawTeamFieldingOverallInseason(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    g = models.IntegerField(blank=True, null=True)
    tc = models.IntegerField(blank=True, null=True)
    po = models.IntegerField(blank=True, null=True)
    a = models.IntegerField(blank=True, null=True)
    e = models.IntegerField(blank=True, null=True)
    fpct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dp = models.IntegerField(blank=True, null=True)
    sba = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    cspct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pb = models.IntegerField(blank=True, null=True)
    ci = models.IntegerField(blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_fielding_overall_inseason'
        unique_together = (('name', 'date'),)


class RawTeamOffenseConference(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_offense_conference'
        unique_together = (('name', 'season'),)


class RawTeamOffenseConferenceInseason(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    date = models.DateField()
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_offense_conference_inseason'
        unique_together = (('name', 'season', 'date'),)


class RawTeamOffenseOverall(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_offense_overall'
        unique_together = (('name', 'season'),)


class RawTeamOffenseOverallInseason(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    date = models.DateField()
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_offense_overall_inseason'
        unique_together = (('name', 'season', 'date'),)


class RawTeamPitchingConference(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    g = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    so_9 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    era = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_pitching_conference'
        unique_together = (('name', 'season'),)


class RawTeamPitchingConferenceInseason(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    date = models.DateField()
    g = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    so_9 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    era = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_pitching_conference_inseason'
        unique_together = (('name', 'season', 'date'),)


class RawTeamPitchingOverall(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    g = models.IntegerField(blank=True, null=True)
    w = models.IntegerField(blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    sv = models.IntegerField(blank=True, null=True)
    cg = models.IntegerField(blank=True, null=True)
    sho = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    era = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wp = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    bk = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    so_9 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_pitching_overall'
        unique_together = (('name', 'season'),)


class RawTeamPitchingOverallInseason(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    date = models.DateField()
    g = models.IntegerField(blank=True, null=True)
    w = models.IntegerField(blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    sv = models.IntegerField(blank=True, null=True)
    cg = models.IntegerField(blank=True, null=True)
    sho = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    er = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    era = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wp = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    bk = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    so_9 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'raw_team_pitching_overall_inseason'
        unique_together = (('name', 'season', 'date'),)


class ReplacementLevel(Base):
    season = models.IntegerField(primary_key=True)
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ops = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bb_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    so_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    iso = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    babip = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sbr = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wsb = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    woba = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wraa = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    off = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wrc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    wrc_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    off_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    off_pa = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'replacement_level'


# class TeamIds(Base):
#     name = models.CharField(max_length=30, blank=True, null=True)
#     id = models.CharField(max_length=5, blank=True, null=True)
#
#     class Meta(Base.Meta):
#         db_table = 'team_ids'


class TeamOffenseOverall(Base):
    name = models.CharField(primary_key=True, max_length=30)
    season = models.IntegerField()
    g = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    x2b = models.IntegerField(blank=True, null=True)
    x3b = models.IntegerField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    rbi = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    tb = models.IntegerField(blank=True, null=True)
    xbh = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    go = models.IntegerField(blank=True, null=True)
    fo = models.IntegerField(blank=True, null=True)
    go_fo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hbp_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bb_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    so_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    babip = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    iso = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    avg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    obp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    slg = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ops = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta(Base.Meta):
        db_table = 'team_offense_overall'
        unique_together = (('name', 'season'),)
