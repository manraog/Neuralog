import speake3

hablar = speake3.Speake()
hablar.set('voice', 'es-mx')
hablar.set('pitch', '20')

hablar.say("je je je")
hablar.talkback()
