
import logging
from decouple import config
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from search_bot_service import busqueda, search_brand_dsct, auto_telegram, delete_brand,add_brand_list,read_category,manual_telegram, search_market_dsct,search_market2_dsct, search_product_dsct_html, test2, search_brand_dsct_html,read_brands


def super_bot( bot_token ,chat, db1,db2):

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


    # async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    ### 1 ENVIA EL STATUS DEL BOT 
    async def getBotInfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola soy un Bot creado para la Nave por Sr Spok. Estoy operativo no te preocupes !")
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId))


    ### 2 ENVIA LOS COMANDOS DEL BOT 
    async def Commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="#################\n LISTA DE COMANDOS\n #################\n \n >Marca y porcentaje (Telegram)\n /b marca %   \n \n >Palabra  y % (HTML)\n /product palabra %\n \n >Tienda y %  (HTML)\n /send tienda %\n \n >Tienda y %  (Telegram)\n /market tienda % \n \n >Codigo de producto (Telegram)\n /cod codigo_de_producto\n \n >Busca y envia variacion o nuevo (Telegram)\n /auto categoria  (Telegram)\n \n >Busca toda categoria 60% (Telegram)\n /manual categoria % (Telegram)\n \n >Agrega marca a categoria(Telegram)\n /brand marca categoria\n \n >Elimina marca a categoria(Telegram)\n /delete marca categoria")
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} ha solicitado informacion de los comandos  " +str(chatId))


    ### 3 SE ECARGA DE DAR AUTOMATICAMENTE LA BIENVENIDA A LOS NUEVOS INTEGRANTES 
    async def welcomeMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chatId = update.message.chat_id
        updateMsg= getattr(update, "message", None)
        for user in updateMsg.new_chat_members:
                userName = user.first_name
        await context.bot.send_message(chat_id=update.effective_chat.id, parse_mode= "HTML", text=f"Bienvenido al grupo {userName}.")
        logging.info(f"el usuario {userName} a ingresado al chat  " +str(chatId))


    ### 4 BUSCA EN BASE A MARCA Y DESCUENTO 
    async def custom_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId))

        brand= (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
        if dsct <= 41:
            dsct = 40
        search_brand_dsct(brand, dsct, bot_token ,chat)
        
    

    # async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     text_caps = ' '.join(context.args).upper()
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


    # async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     query = update.inline_query.query
    #     if not query:
    #         return
    #     results = []
    #     results.append(
    #         InlineQueryResultArticle(
    #             id=query.upper(),
    #             title='Caps',
    #             input_message_content=InputTextMessageContent(query.upper())
    #         )
    #     )
    #     await context.bot.answer_inline_query(update.inline_query.id, results)

    # async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text="No es un comando Valido recontra Gil...")





    if __name__ == '__main__':
        application = ApplicationBuilder().token(bot_token).build()
        

        # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
        botinfo = CommandHandler('botinfo', getBotInfo)
        application.add_handler(botinfo)

        commads = CommandHandler('comandos', Commands)
        application.add_handler(commads)

        custom_se = CommandHandler('b', custom_search)
        application.add_handler(custom_se)




        # caps_handler = CommandHandler('caps', caps)
        # inline_caps_handler = InlineQueryHandler(inline_caps)
        # unknown_handler = MessageHandler(filters.COMMAND, unknown)
        # application.add_handler(unknown_handler)


        # application.add_handler(inline_caps_handler)

        # application.add_handler(caps_handler)

        
        # application.add_handler(echo_handler)
        
        application.run_polling()


# chat = config("EXCELSIOR_CHAT_TOKEN")
# bot_token = config("TOKEN_PICARD")
# db1 = "excelsior1"
# db2 = "excelsior2"

# super_bot( bot_token ,chat, db1,db2)