
close_prompt_template = "嗯，那对于'{}'这个问题，请你从['完全同意', '基本同意', '部分同意', '既不同意也不否认', '不太同意', '基本不同意', '完全不同意']中选择一个适合你的选项。请务必用中文回答，并用单引号强调你的选项。"

bigfive_scale_prompt_template = """
You will read a psychological assessment report. This psychological assessment report assesses whether the subject has a high {} personality.Based on this report, output a jsoncontaining two fields: score and reasonscore is between -5 to 5 pointsIf the subject shows high {} personality in many factors, the score is 5 pointsIf the subject shows high {} personality in a single factor, the score is 2 pointsIf the report is unable to determine the subject's personality, the score is 0 pointsIf the subject shows low {} personality in a single factor, the score is -2 pointsIf the subject shows low {} personality in many factors, the score is -5 points. 
Reason is a brief summary of the reportOnly output the json, do not output any additional information, Expecting property name enclosed in double quotesReport:
"""

mbti_assess_prompt_template_wo_percent = '''You are an expert in MBTI. I am conducting an MBTI test on someone. My goal is to gauge their position on the {} spectrum of the MBTI through a series of open-ended questions. For clarity, here's some background on differentiating this particular dimension:
===
{}
===

I've invited a participant, {}, and had the following conversations in Chinese:
===
{}
===

Please help me distinguish whether {} leans more towards the {} or {} category within the MBTI's {} dimension. Please output in the following json format:
===
{{
    "analysis": <your analysis in Chinese, based on the conversations>,
    "result": <your result, either "{}" or "{}">
}}
'''

bigfive_assess_prompt_template = '''You are a psychologist with expertise in personality theories. I'm conducting an experiment to evaluate participants' scores in the Big Five personality traits, especially on the {} dimension. For clarity, here's some background on differentiating this particular dimension and its factors:
===
{}
===

I've invited a participant, {}, and had the following conversations in Chinese:
===
{}
===

Please help me evaluates whether {} possesses a high {} personality or a low {} personality, and provide an integer score ranging from -5 to 5. 

Below are some scoring references. If the subject demonstrates a high {} personality in many factors, the score is 5 points. If the subject exhibits a high {} personality in a single factor, the score is 2 points. If the subject's personality cannot be determined, the score is 0 points. If the subject shows a low {} personality in one factor, the score is -2 points. If the subject indicates a low {} personality across multiple factors, the score is -5 points. 

Please output in the following json format:
===
{{
    "analysis": <your analysis in Chinese, based on the conversations>,
    "result": <the person's score on {}, ranging from -5 to 5>
}}
===
'''

mbti_assess_prompt_template = '''You are an expert in MBTI. I am conducting an MBTI test on someone. My goal is to gauge their position on the {} spectrum of the MBTI through a series of open-ended questions. For clarity, here's some background on differentiating this particular dimension:
===
{}
===

I've invited a participant, {}, and had the following conversations in Chinese:
===
{}
===

Please help me distinguish whether {} leans more towards the {} or {} category within the MBTI's {} dimension. You should provide the person's percentage of each category, which sums to 100%, e.g., 30% A and 70% B. 
Please output in the following json format:
===
{{
    "analysis": <your analysis in Chinese, based on the conversations>,
    "result": {{ "{}": <percentage 1>, "{}": <percentage 2> }} (The sum of percentage 1 and percentage 2 should be 100%. Output without percent sign.) 
}}
'''

mbti_dimension_prompt = {
    'E/I': '''E/I Dimension: Extraversion (E) vs Introversion (I)

E (Extraversion): Extraverts draw energy from interacting with others. They feel comfortable in social settings and tend to express their thoughts. Extraverts are often more active, seek social stimulation, and enjoy participating in group activities. For them, connecting with people, sharing, and exchanging ideas is often a need. They might be more focused on external world stimuli, such as sounds, colors, and social dynamics.

I (Introversion): Introverts feel more comfortable when alone. They derive energy from inner reflection and personal time. Contrary to extraverts, prolonged social interaction might tire them. Introverts might be more introspective, enjoy deep thinking, and tend to have meaningful personal relationships. They are more concerned with the inner world, such as thoughts, emotions, and imaginations.''',

    'S/N': '''S/N Dimension: Sensing (S) vs Intuition (N)

S (Sensing): Sensing individuals value the concrete, practical, and present situations. They rely on their five senses to process information and often focus on details. For them, past experiences and tangible evidence play a significant role in decision-making. They are typically pragmatic and tend to deal with what they "see" and "hear".

N (Intuition): Intuitive individuals tend to focus on potential possibilities and future opportunities. They like to think about "what could be", rather than just "what is". They lean more towards abstract thinking and can capture concepts and patterns effectively. Intuitives are often more innovative, preferring new ideas and approaches.''',

    'T/F': '''T/F Dimension: Thinking (T) vs Feeling (F)

T (Thinking): Thinking individuals rely primarily on logic and analysis when making decisions. They pursue fairness and objectivity and might be more direct and frank. For them, finding the most efficient method or the most logical solution is crucial, even if it might hurt some people's feelings.

F (Feeling): Feeling individuals consider people's emotions and needs more when making decisions. They strive for harmony, tend to build relationships, and avoid conflicts. They are often more empathetic, valuing personal values and emotions, rather than just facts or logic.''',

    'P/J': '''P/J Dimension: Perceiving (P) vs Judging (J)

P (Perceiving): Perceivers are more open and flexible. They tend to "go with the flow" rather than overly planning or organizing things. Perceivers like to explore various possibilities and prefer to leave options open to address unforeseen circumstances. They lean towards postponing decisions to gather more information and better understanding. For them, life is a continuous process of change, not an event with fixed goals or plans. They often focus more on the experience itself rather than just the outcome.

J (Judging): Judging individuals are more structured and planned in their lives. They prefer clear expectations and structures and often set goals and pursue them. Judgers are usually more organized and tend to make decisions in advance. They like to act according to plans and feel comfortable in an orderly environment. For them, achieving goals and completing tasks are often priorities. They might focus more on efficiency and structure rather than openness or spontaneity.'''
}

to_option_prompt_template= '''You are an expert in MBTI. I am conducting an MBTI test on someone. I've invited a participant, {}, and asked a question in Chinese. Please help me classify the participant's response to this question into one the the following options: ['fully agree', 'generally agree', 'partially agree', 'neither agree nor disagree', 'partially disagree', 'generally disagree', 'fully disagree'] 

Please output in the json format as follows:
===
{{
"analysis": <your analysis in Chinese, based on the conversations>,
"result": <your result from ['fully agree', 'generally agree', 'partially agree', 'neither agree nor disagree', 'partially disagree', 'generally disagree', 'fully disagree']>
}}
===
The question and response is as follows, where {} is my name:
'''

bigfive_dimension_prompt = {}

bigfive_dimension_prompt['conscientiousness'] = """Conscientiousness refers to the way we control, regulate, and direct our impulses. It assesses organization, persistence, and motivation in goal-directed behavior. It contrasts dependable, disciplined individuals with those who are lackadaisical and disorganized. Conscientiousness also reflects the level of self-control and the ability to delay gratification. Impulsiveness is not necessarily bad, sometimes the environment requires quick decision-making. Impulsive individuals are often seen as fun, interesting companions. However, impulsive behavior often gets people into trouble, providing momentary gratification at the expense of long-term negative consequences, such as aggression or substance abuse. Impulsive people generally do not accomplish major achievements. Conscientious people more easily avoid trouble and achieve greater success. They are generally seen as intelligent and reliable, although highly conscientious people may be perfectionists or workaholics. Extremely prudent individuals can seem monotonous, dull, and lifeless.

Conscientiousness can be divided into six facets:

C1 COMPETENCE

Refers to the sense that one is capable, sensible, prudent, and effective. High scorers feel well-prepared to deal with life. Low scorers have a lower opinion of their abilities, admitting that they are often unprepared and inept.

High scorers: Confident in own abilities. Efficient, thorough, confident, intelligent.

Low scorers: Lack confidence in own abilities, do not feel in control of work and life. Confused, forgetful, foolish.

C2 ORDER

High scorers are neat, tidy, well-organized, they put things in their proper places. Low scorers cannot organize things well, describe themselves as unmethodical.

High scorers: Well-organized, like making plans and following them. Precise, efficient, methodical.

Low scorers: Lack planning and orderliness, appear haphazard. Disorderly, impulsive, careless.

C3 DUTIFULNESS

To some extent, dutifulness refers to adherence to one's conscience, assessed by this facet. High scorers strictly follow their moral principles and scrupulously fulfill their moral obligations. Low scorers are more casual about such matters, somewhat unreliable or undependable.

High scorers: Dutiful, follow the rules. Reliable, polite, organized, thorough.

Low scorers: Feel restricted by rules and regulations. Often seen by others as unreliable, irresponsible. Careless, thoughtless, distracted.

C4 ACHIEVEMENT STRIVING

High scorers have high aspiration levels and work hard to achieve their goals. They are industrious, purposeful, and have a sense of direction. Low scorers are lackadaisical, even lazy, lacking motivation to succeed, having no ambitions and appearing to drift aimlessly. But they are often quite satisfied with their modest level of accomplishment.

High scorers: Striving for success and excellence, often seen as workaholics. Ambitious, industrious, enterprising, persevering.

Low scorers: Satisfied with completing basic tasks, seen as lazy by others. Leisurely, daydreaming, aimless.

C5 SELF-DISCIPLINE

Refers to the ability to begin tasks and follow through despite boredom or distractions. High scorers can motivate themselves to get the job done. Low scorers procrastinate in starting routine chores, easily losing confidence and giving up.

Low scorers: Procrastinate in work, often do not finish tasks, easily discouraged by obstacles. Unambitious, forgetful, distracted.

C6 DELIBERATION

This facet pertains to the tendency to think carefully before acting. High scorers are cautious and deliberate. Low scorers are hasty and speak/act without considering consequences.

High scorers: Think before acting, not impulsive. Prudent, logical, mature.

Low scorers: Act without considering consequences, impulsive, speak thoughts as they occur. Immature, rash, impulsive, careless.
"""

bigfive_dimension_prompt['openness'] = """Openness describes a person's cognitive style. Openness to experience is defined as: the proactive seeking and appreciation of experience for its own sake, and tolerance for and exploration of the unfamiliar. This dimension contrasts intellectually curious, creative people open to novelty with traditional, down-to-earth, closed-minded individuals lacking artistic interests. Open people prefer abstract thinking, have wide interests. Closed people emphasize the concrete, conventional, are more traditional and conservative. Open people are suited to professions like teaching, closed people to occupations like police, sales, service.

Openness can be divided into six facets:

O1 FANTASY

Open people have vivid imaginations and active fantasy lives. Their daydreams are not just escapes, but ways to create interesting inner worlds. They elaborate and flesh out their fantasies, and believe imagination is essential for a rich, creative life. Low scorers are more prosaic, keeping their minds on the task at hand.

High scorers: Find the real world too plain and ordinary. Enjoy imagining, creating a more interesting, enriching world. Imaginative, daydreaming.

Low scorers: Matter-of-fact, prefers real-world thinking. Practical, prefer concrete thought.

O2 AESTHETICS

High scorers have deep appreciation for art and beauty. They are moved by poetry, absorbed in music, and touched by art. They may not have artistic talent or refined taste, but most have strong interests that enrich their experience. Low scorers are relatively insensitive and indifferent to art and beauty.

High scorers: Appreciate beauty in nature and the arts. Value aesthetic experiences, touched by art and beauty.

Low scorers: Insensitive to beauty, disinterested in the arts. Insensitive to art, cannot understand it.

O3 FEELINGS

Refers to receptivity to one's own inner feelings, evaluating emotions as an important part of life. High scorers experience deeper emotional states and can differentiate among them, experiencing happiness and unhappiness more intensely than others. Low scorers have blunted affect and do not believe feelings are important.

High scorers: Aware of own emotions/inner life. Sensitive, empathic, give importance to own feelings.

Low scorers: Little access to own emotions/inner world, unwilling to articulate them. Narrow range of emotions, insensitive to context.

O4 ACTIONS

Openness is seen behaviorally as willingness to try different activities, visit new places, or sample exotic foods. High scorers prefer novelty and variety to familiarity and routine. Over time, one high scorer may have a wide array of interests. Low scorers find change difficult and prefer to stick with known activities.

High scorers: Like experiencing new things, traveling, seeking different experiences. Find routine boring, willing to try new things. Seek novelty/variety, try new activities.

Low scorers: Uncomfortable with unfamiliar, prefer familiar surroundings/people. Set in ways, like familiar things.

O5 IDEAS

Intellectual curiosity is an aspect of openness, manifested both in pursuit of intellectual interests for their own sake and in open-mindedness to new, unconventional ideas. High scorers enjoy philosophical arguments and brain teasers. Low scorers have narrower intellectual interests, and even if they are intelligent concentrate their abilities within limited areas.

High scorers: Inquisitive, analytical, theoretical.

Low scorers: Pragmatic, fact-oriented, unappreciative of mental challenges.

O6 VALUES

Openness to values means constantly reexamining social, political, and religious values. Closed people tend to accept authority, honor tradition, and as a result are conservative regardless of political affiliation.

High scorers: Enjoy challenging authority, convention, traditional ideas. At the extreme, show hostility toward rules, sympathize with law-breakers. Tolerant, broad-minded, nonconforming.

Low scorers: Prefer the stability and security of authority and convention, unwilling to challenge the status quo. Dogmatic, conservative, conforming.
"""


bigfive_dimension_prompt['agreeableness'] = """Agreeableness assesses the degree to which an individual is likable, while Agreeableness examines an individual's attitudes toward others, encompassing both a compassionate, sympathetic orientation along with antagonism, distrust, indifference. This facet represents the broad interpersonal orientation. Agreeableness represents "love", how much value is placed on cooperation and social harmony.

High scorers are good-natured, friendly, generous, helpful, willing to compromise their interests for others. They have an optimistic view of human nature, believing others to be honest, decent and trustworthy. Low scorers place self-interest above helping others. They are generally unconcerned with others' well-being and therefore unwilling to extend themselves for others. At times, they are overly suspicious of others' motives. For certain occupations, high agreeableness may not be optimal, especially when toughness and objective judgment is required, such as scientists, critics, and soldiers.

Agreeableness can be divided into six facets:

A1 TRUST

High scorers believe others are honest and well-intentioned. Low scorers tend to be cynical and suspicious, assuming others to be dishonest and dangerous.

High scorers: Believe others to be honest, reliable and well-meaning. Forgiving, trusting of others, good-natured.

Low scorers: View others as selfish, dangerous, looking to take advantage. Cautious, pessimistic, suspicious, hardhearted.

A2 STRAIGHTFORWARDNESS

High scorers are frank, sincere, ingenuous. Low scorers are more willing to manipulate others through flattery, craftiness, deception. They see it as an essential social skill and view straightforward people as naive.

High scorers: Believe there is no need for pretense in dealing with others, appear straightforward, genuine. Direct, frank, open, ingenuous.

Low scorers: Tend to be guarded in dealings with others, defensive, unwilling to reveal their full hand. Shrewd, slick, charming.

A3 ALTRUISM

High scorers actively concern themselves with others' welfare as evidenced by generosity, consideration of others, and a willingness to assist those in need. Low scorers are more self-centered and reluctant to get involved in others' problems.

High scorers: Willing to assist others, find helping others rewarding. Warm-hearted, soft-hearted, mild-mannered, generous, kindhearted.

Low scorers: Unwilling to help others, find helping a burden. Selfish, misanthropic, hardhearted, ungenerous.

A4 COMPLIANCE

Relates to personality in the context of interpersonal conflict. High scorers tend to defer to others, inhibit aggression, forgive and forget. Compliant people are gentle, mild-mannered. Low scorers are aggressive, preferring competition over cooperation, and unhesitatingly express anger when necessary.

High scorers: Dislike conflict with others, willing to give up their own standpoint or deny their own needs to get along. Deferent, accommodating, obliging.

Low scorers: Do not mind conflict with others, willing to intimidate others to achieve their goals. Stubborn, making unreasonable demands, obstinate, hardhearted.

A5 MODESTY

High scorers are self-effacing, humble. Low scorers believe they are superior and may be seen by others as arrogant, egotistical.

High scorers: Modest, unassuming.

Low scorers: Assertive, arrogant, vain, rude.

A6 TENDER-MINDEDNESS

Measures attitudes of sympathy and concern for others. High scorers are moved by others' needs and advocate humane social policies. Low scorers are hardheaded, unmoved by appeals to pity. They pride themselves on making objective appraisals based on cool logic.

High scorers: Sympathetic, moved by others' suffering, express pity. Friendly, warm-hearted, gentle, soft-hearted.

Low scorers: Do not strongly feel others' pain, pride themselves on objectivity, more concerned with truth and fairness than mercy. Callous, hardhearted, opinionated, ungenerous.
"""

bigfive_dimension_prompt['extraversion'] = """Extraversion represents the quantity and intensity of interpersonal interaction, the need for stimulation, and capacity for joy. This dimension contrasts social, outgoing, action-oriented individuals with reserved, sober, shy, silent types. This trait can be measured through two facets: the level of interpersonal involvement and the activity level. The former evaluates the degree to which an individual enjoys the company of others. The latter reflects an individual's personal pace and vigor.

Extraverted people enjoy interacting with others, are full of energy, and often experience positive emotions. They are enthusiastic, enjoy physical activities, and like excitement and adventure. In a group, they are very talkative, confident, and enjoy being the center of attention.

Introverted people are quieter, more cautious, and do not enjoy too much interaction with the outside world. Their lack of desire for interaction should not be confused with shyness or depression, it is simply because compared to extraverts, they do not need as much stimulation and prefer being alone. An introvert's tendencies are sometimes wrongly viewed as arrogance or unfriendliness, but they are often very kind people once you get to know them.

Extraversion can be divided into the following six facets:

E1 WARMTH

Most relevant to interpersonal intimacy. Warm people are affectionate and friendly. They genuinely like others and easily form close relationships. Low scorers are not necessarily hostile or lacking in compassion, but are more formal, reserved, and detached in their behavior.

High scorers: Warm people enjoy those around them and often express positive, friendly emotions towards others. They are good at making friends and forming intimate relationships. Sociable, talkative, affectionate.

Low scorers: Although not necessarily cold or unfriendly, they are often seen as distant by others.

E2 GREGARIOUSNESS

Refers to a preference for other people's company. Gregarious people enjoy the company of others and the more people the merrier. Low scorers tend to be loners, they do not seek out and even actively avoid social stimulation.

High scorers: Enjoy being with people, prefer lively, crowded settings. Outgoing, having many friends, seek social affiliations.

Low scorers: Avoid crowds, find them draining. Prefer having more time alone, having their own personal space. Avoid crowds, enjoy solitude.

E3 ASSERTIVENESS

High scorers are dominant, forceful, and socially ascendant. They speak without hesitation and often become group leaders. Low scorers prefer to stay quietly in the background and let others do the talking.

High scorers: Like occupying a position of social dominance, directing others, influencing others' behavior. Dominant, forceful, confident, decisive.

Low scorers: Talk little in groups, allow others to occupy the dominant role. Modest, shy, quiet, reserved.

E4 ACTIVITY

High scorers lead fast-paced, vigorous lives, are energetic, and have a need to keep busy. Low scorers are more leisurely and relaxed, but not necessarily lazy or sluggish.

High scorers: Fast-paced, busy in work and life. Appear energetic, enjoy participating in many activities. Energetic, fast-paced, vigorous.

Low scorers: Slow-paced, leisurely in work and life. Unhurried, deliberate, composed.

E5 EXCITEMENT SEEKING

High scorers crave excitement and stimulation, enjoy bright colors and noisy environments. Excitement seeking is akin to some aspects of sensation seeking. Low scorers have little need for thrills and prefer activities seen as dull by the former.

High scorers: Easily get bored without stimulation, enjoy loud music/noise, like adventure, seek thrills. Flashy, seek intense experiences, thrill-seeking.

Low scorers: Avoid noise and crowds, dislike risky ventures. Cautious, sedate, not interested in thrills.

E6 POSITIVE EMOTIONS

Reflects the tendency to experience positive emotions (joy, happiness, love, excitement).

High scorers: Easily experience various positive moods like joy, optimism, excitement. Cheerful, elated, optimistic.

Low scorers: Do not readily experience positive emotions, but does not mean they often feel negative emotions either. Low scorers are simply less prone to excitement. Unemotional, calm, serious.
"""

bigfive_dimension_prompt['neuroticism'] = """Neuroticism or Emotional Stability: Having tendencies of anxiety, hostility, depression, self-consciousness, impulsiveness, vulnerability.

N1 ANXIETY

Anxious individuals tend to worry, fear, be easily concerned, tense, and oversensitive. Those who score high are more likely to have free-floating anxiety and apprehension. Those with low scores tend to be calm, relaxed. They do not constantly worry about things that might go wrong.

High scorers: Anxiety, easily feel danger and threats, tend to be tense, fearful, worried, uneasy.

Low scorers: Calm state of mind, relaxed, not easily scared, won't always worry about things that could go wrong, emotions are calm, relaxed, stable.

N2 ANGRY HOSTILITY

Reflects the tendency to experience anger and related states (e.g. frustration, bitterness). Measures the ease with which an individual experiences anger.

High scorers: Easily angered, resentful when feeling unfairly treated, irritable, angry, frustrated.

Low scorers: Not easily angered/provoked, friendly, even-tempered, not easily provoked to anger.

N3 DEPRESSION

Measures individual differences in the tendency to experience depressive affect. High scorers are prone to feelings of guilt, sadness, hopelessness, and loneliness. They are easily discouraged and often feel blue. Low scorers rarely experience these emotions.

High scorers: Despairing, guilty, gloomy, dejected. Prone to feeling sorrow, abandonment, discouraged. Prone to feelings of guilt, sadness, disappointment, and loneliness. Easily discouraged, often feeling down.

Low scorers: Not prone to feeling sad, rarely feels abandoned.

N4 SELF-CONSCIOUSNESS

Core is shyness and embarrassability. Such individuals feel uncomfortable in groups, are sensitive to ridicule, and prone to feelings of inferiority. Self-consciousness is similar to shyness and social anxiety. Low scorers are not necessarily well-mannered or skilled socially, they are simply less disrupted by awkward social situations.

High scorers: Too concerned with what others think, afraid of being laughed at, tend to feel shy, anxious, inferior, awkward in social situations.

Low scorers: Composed, confident in social situations, not easily made tense or shy.

N5 IMPULSIVENESS

Refers to control over cravings and urges. Individuals give in too easily to impulses and temptations to care for long-term consequences (e.g. for food, cigarettes, possessions), although they will regret their actions later. Low scorers are better able to resist temptation and have higher frustration tolerance.

High scorers: Cannot resist cravings when experiencing strong urges, tend to pursue short-term satisfaction without considering long-term consequences. Cannot resist temptations, rash, spiteful, self-centered.

Low scorers: Self-controlled, can resist temptation.

N6 VULNERABILITY

Refers to susceptibility to stress. High scorers have difficulty coping with stress, become dependent, hopeless, panicked when facing emergencies. Low scorers feel that they can handle difficult situations properly.

High scorers: Under stress, easily feel panic, confusion, helpless, cannot cope with stress.

Low scorers: Under stress, feel calm, confident. Resilient, clear-headed, brave."""

