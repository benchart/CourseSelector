from chatbotModel import ChatbotModel

model = ChatbotModel()


INTEREST_OPTIONS = [
    "Mathematics",
    "Creative Writing",
    "Biology",
    "Robotics",
    "Music Theory",
    "World History",
    "Computer Programming",
    "Environmental Science",
    "Public Speaking",
    "Theater Arts",
    "Astronomy",
    "Psychology",
    "Film Studies",
    "Chemistry",
    "Political Science",
    "Entrepreneurship",
    "Photography",
    "Philosophy",
    "Statistics",
    "Debate",
    "Forensic Science",
    "Sociology",
    "Graphic Design",
    "Economics",
    "Physics",
    "Marine Biology",
    "UX Design",
    "Digital Media",
    "Artificial Intelligence",
    "Game Development",
    "Ethics",
    "Anthropology",
    "Web Development",
    "Linguistics",
    "Cognitive Science",
    "Marketing",
    "Botany",
    "Data Science",
    "Education Policy",
    "Foreign Languages",
    "Geology",
    "Journalism",
    "Music Performance",
    "Gender Studies",
    "Classical Studies",
    "Animation",
    "Social Work",
    "Nanotechnology",
    "Criminal Justice",
    "Zoology"
]

INTERESTS_BY_DESCRIPTION = [
    "hello",
    "hello"
]

class_descriptions = [
    "Introduction to Computer Science: A foundational course in programming, algorithms, and problem-solving.",
    "Calculus I: Study of limits, derivatives, and integrals, focusing on single-variable functions.",
    "Psychology 101: An overview of the basics of psychology, including behavioral science, cognition, and development.",
    "Introduction to Philosophy: Exploration of major philosophical ideas, thinkers, and ethical dilemmas.",
    "Chemistry 101: Basic principles of chemistry, including atomic structure, chemical reactions, and stoichiometry.",
    "Microeconomics: Introduction to economic theory, including supply and demand, market structures, and government intervention.",
    "World History: Survey of major events and developments from ancient to modern times across different cultures.",
    "Statistics for Social Sciences: Introduction to statistics with applications in social research and data analysis.",
    "English Literature: Study of classic and contemporary works of fiction, poetry, and drama from various cultures.",
    "Introduction to Sociology: Exploration of social structures, institutions, and processes that shape human behavior.",
    "Biology 101: Fundamentals of biology, including cell biology, genetics, and ecological systems.",
    "Public Speaking: Develop skills in delivering persuasive, informative, and effective speeches.",
    "Physics I: Introduction to the fundamental concepts of physics, including mechanics, motion, and energy.",
    "Business Management: Study of business principles, including leadership, strategic planning, and organizational behavior.",
    "Art History: Survey of the evolution of art from prehistoric times to the present, focusing on different periods and movements.",
    "Advanced Calculus: A deeper dive into multi-variable calculus and its applications in real-world scenarios.",
    "Environmental Science: Examination of ecological systems, environmental challenges, and sustainable practices.",
    "Political Science 101: Introduction to political theory, systems, and institutions at the national and global levels.",
    "Ethics in Technology: Exploration of the ethical challenges and dilemmas in the rapidly evolving tech industry.",
    "Creative Writing: A course designed to help students develop their writing skills in fiction, poetry, and creative non-fiction."
    ]

model.callChatbot(F"create a python dictionary mapping each class description in {class_descriptions} to one or more interests in {INTEREST_OPTIONS}")