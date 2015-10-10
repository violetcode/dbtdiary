from django.db import models
from django.contrib.auth.models import User

VALUE_CHOICES = (
	(0, '0'),
	(1, '1'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5')
)

SKILLS_CHOICES = (
	("Wise Mind", "Wise Mind"),
	("Observe (Urge Surfing)", "Observe (Urge Surfing)"),
	("Describe: put words on", "Describe: put words on"),
	("Participate : enter the experience", "Participate: enter the experience"),
	("Nonjudgemental stance", "Nonjudgemental stance"),
	("One-mindfully: in-the-moment", "One-mindfully: in-the-moment"),
	("Effectiveness: focus on what works", "Effectiveness: focus on what works"),
	("Objective Effectiveness: DEAR MAN", "Objective Effectiveness: DEAR MAN"),
	("Relationship Effectiveness: GIVE", "Relationship Effectiveness: GIVE"),
	("Self-respect Effectiveness: FAST", "Self-respect Effectiveness: FAST"),
	("Reduce Vulnerability: PLEASE", "Reduce Vulnerability: PLEASE"),
	("Build MASTERY", "Build MASTERY"),
	("Build positive experiences", "Build positive experiences"),
	("Opposite-to-emotion action", "Opposite-to-emotion action"),
	("Distract (Adaptive Denial)", "Distract (Adaptive Denial)"),
	("Self-soothe", "Self-soothe"),
	("Improve the moment", "Improve the moment"),
	("Pros and cons", "Pros and cons"),
	("Radical Acceptance", "Radical Acceptance"),
	("Building Structure: Work", "Building Structure: Work"),
	("Building Structure: Love", "Building Structure: Love"),
	("Building Structure: Time", "Building Structure: Time"),
	("Building Structure: Place", "Building STructure: Place"),
	("Take nothing personally", "Take nothing personally"),
	("Always do your best", "Always do your best"),
	("Don't make assumptions", "Don't make assumptions"),
	("Be impeccable with your word", "Be impeccable with your word")
)

SKILL_VALUES_CHOICES = (
	(0, "0 - Not thought about or used"),
	(1, "1 - Thought about, not used, didn't want to"),
	(2, "2 - Thought about, not used, wanted to"),
	(3, "3 - Tried but couldn't use them"),
	(4, "4 - Tried, could do them but they didn't help"),
	(5, "5 - Tried, could use them, helped"),
	(6, "6 - Didn't try, used them, didn't help"),
	(7, "7 - Didn't try, used them, helped")
)

class UsedSkills(models.Model):
	description = models.CharField(max_length=100, choices=SKILLS_CHOICES)
	
	def __unicode__(self):
		return self.description
	
	class Meta:
		verbose_name_plural = 'Used Skills'
		ordering = ['id']
	
class Diary(models.Model):
	user = models.ForeignKey(User)
	time = models.DateTimeField(auto_now_add=True)
	used_skills = models.ManyToManyField(UsedSkills, blank=True,)
	#used_skills = models.CharField(max_length=100 ,choices=SKILLS_CHOICES, blank=True, null=True)
	urge_suicide = models.IntegerField(choices=VALUE_CHOICES, default=0)
	urge_sh = models.IntegerField(choices=VALUE_CHOICES, default=0)
	pain = models.IntegerField(choices=VALUE_CHOICES, default=0)
	sad = models.IntegerField(choices=VALUE_CHOICES, default=0)
	shame = models.IntegerField(choices=VALUE_CHOICES, default=0)
	anger = models.IntegerField(choices=VALUE_CHOICES, default=0)
	fear = models.IntegerField(choices=VALUE_CHOICES, default=0)
	disgust = models.IntegerField(choices=VALUE_CHOICES, default=0)
	jealousy = models.IntegerField(choices=VALUE_CHOICES, default=0)
	guilt = models.IntegerField(choices=VALUE_CHOICES, default=0)
	agitation = models.IntegerField(choices=VALUE_CHOICES, default=0)
	action_sh = models.BooleanField()
	lying = models.IntegerField(default=0)
	joy = models.IntegerField(choices=VALUE_CHOICES, default=0)
	happy = models.IntegerField(choices=VALUE_CHOICES, default=0)
	content = models.IntegerField(choices=VALUE_CHOICES, default=0)
	calm = models.IntegerField(choices=VALUE_CHOICES, default=0)
	grateful = models.IntegerField(choices=VALUE_CHOICES, default=0)
	excitement = models.IntegerField(choices=VALUE_CHOICES, default=0)
	hope = models.IntegerField(choices=VALUE_CHOICES, default=0)
	confidence = models.IntegerField(choices=VALUE_CHOICES, default=0)
	optimism = models.IntegerField(choices=VALUE_CHOICES, default=0)
	skills = models.IntegerField(choices=SKILL_VALUES_CHOICES, default=0)
	notes = models.CharField(max_length=100000, blank=True)
	mood = models.DecimalField(max_digits=5, decimal_places=2, default=0)

	def __unicode__(self):
		return "Entry by %s on %s" % (self.user, self.time,)

	class Meta:
		verbose_name_plural = 'Diary Entries'

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.user

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])