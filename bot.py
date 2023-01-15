
import logging
from decouple import config
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from search_bot_service import busqueda, search_brand_dsct, auto_telegram, delete_brand,add_brand_list,read_category,manual_telegram, search_market_dsct,search_market2_dsct, search_product_dsct_html, test2, search_brand_dsct_html,read_brands
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
import os


def super_bot2( TOKEN, bot_token ,chat, db1,db2):
    print(bot_token)
    print(chat)


    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
   
 

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
    # async def welcomeMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     chatId = update.message.chat_id
    #     updateMsg= getattr(update, "message", None)
    #     for user in updateMsg.new_chat_members:
    #             userName = user.first_name
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bienvenido al grupo {userName}.")
    #     logging.info(f"el usuario {userName} a ingresado al chat  " +str(chatId))


    ### 4 BUSCA EN BASE A MARCA Y DESCUENTO 
    async def custom_search(update: Update, context: ContextTypes.DEFAULT_TYPE ):
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId))

        brand= (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
        if dsct <= 41:
            dsct = 40
        search_brand_dsct(brand, dsct, bot_token ,chat)
        
### 5 BUSCA EN BASE A MARKET Y DESCUENTO
    async def custom_search_market(update: Update, context: ContextTypes.DEFAULT_TYPE):

        market= (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
        dsct = int(dsct)
        if dsct <= 41:
           dsct = 40
        
        search_market_dsct(str(market), int(dsct), bot_token ,chat)

        logging.info(f"marca "+ market + "dsct "+ str(dsct))

        msg="Se realizo busqueda de la marca ingresada"+ str(market) +" de "+ str(dsct) + "%  a mas\n\n#####################################\n#####################################"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

       
### 7 BUSCA EN PRODUCTO CON EL CODIGO SKU
    async def sku(update: Update, context: ContextTypes.DEFAULT_TYPE):

        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName}  busca codigo especifico")
        codigo = context.args[0]
        
        busqueda(str(codigo), bot_token ,chat)
        
        
        keyboard = [
                    [
                        InlineKeyboardButton("Link al producto", callback_data="1"),
                        InlineKeyboardButton("prueba", callback_data="2"),
                    ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg= "Termino la busqueda... si no hay nada no encontre ps"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_markup)
        data = reply_markup.answer()

        if data ==1:
            print("sasadasdasd")
        
        #await context.bot.send_message(chat_id=update.effective_chat.id, text=busqueda(str(codigo), bot_token ,chat),  reply_markup=reply_markup)








### 8 BUSCA AUTOMATICAMENTE LAS MARCAS EN LAS CATEGORIAS DEL 60% EN ADELANTE NO ENVIA SI YA SE ENVIO
    async def auto_tele(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName}  busqueda automatica")
        category=str(context.args[0])

        msg= "Espera un momento se esta procesando la solicitud"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

        auto_telegram( category,db1, db2 ,bot_token ,chat)


### 9 ENVIA PRODUCTOS QUE HAY EN UNA CARTEGORIAS 
    async def category_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} ha solicitado la lista de categorias")
        read_category(bot_token ,chat)

        msg= "Se solicito list de categorias"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

        read_category(bot_token ,chat)

### 10  MUESTRA LAS MARCAS DE CIERTA CATEGORIA
    async def brand_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} ha solicitado  lista de marcas")
        category=context.args[0]
        read_brands(category,bot_token ,chat)

        msg= "Se solicito lista de marcas"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        read_category(bot_token ,chat)

### 11  ANADE LA MARCA A CIERTA CATEGORIA
    async def add_brand(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} se agrego marca a categoria")
        brand= (context.args[0]).replace("%"," ")
        category=(context.args[1]).replace("%","")
        

        msg= "Se agrego " +brand+  " a la categoria "+ category
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        add_brand_list(brand, category,bot_token ,chat)

### 12 ELIMINA MARCA DE CARTEGORIA
    async def brand_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} se agrego marca a categoria")
        brand= (context.args[0]).replace("%"," ")
        category=(context.args[1]).replace("%","")
        

        msg= "Se elimino " +brand+  " de la categoria "+ category
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        delete_brand(brand,category,bot_token ,chat)


### 13 BUSCA TODAS LAS MARCAS SEGUN CATEGORIA MANUALMENTE CON DESCUENTO PERSONALIZADO
    async def auto_tele_dsct(update: Update, context: ContextTypes.DEFAULT_TYPE):
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName}  buscqueda  marca y dsct")
        category=str(context.args[0])
        dsct=int(context.args[1])

        msg= "Espera un momento se esta procesando la solicitud"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

        manual_telegram( category,dsct ,bot_token ,chat)

        msg= "Se termino la busqueda " 
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


### 14 CREA HTML DE BUSQUEDA DE MARKET Y DSCT PERSONALIZADO
    async def send_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} ha solicitado una buesqueda")

        market = (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
        dsct = int(dsct)
        try:
         price = (context.args[2])
        except: price = None

        search_market2_dsct(market,dsct,price, bot_token ,chat)

        document = open(config("HTML_PATH")+market+".html", 'rb')
        await context.bot.send_document(chat, document)
        document.close()
        os.remove(config("HTML_PATH")+market+".html")


### 15 CREA HTML DE BUSQUEDA DE PALABRA CONTENIDA EN EL NOMBRE DEL PRODUCTO Y DSCT PERSONALIZADO POSIBLE ORDENAR PRECIO MAYOR A MENOR
    async def send_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} ha solicitado una buesqueda")

        product = (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
    
        try:
         price = (context.args[2])
        except: price = None
        
        search_product_dsct_html(product,dsct,price ,bot_token ,chat)

        document = open(config("HTML_PATH")+"producto.html", 'rb')
        await context.bot.send_document(chat, document)
        document.close()
        os.remove(config("HTML_PATH")+"producto.html")




### 16 CREA HTML DE BUSQUEDA DE MARCA Y DSCT PERSONALIZADO
    async def brand_to_html(update: Update, context: ContextTypes.DEFAULT_TYPE):
        userName = update.effective_user["first_name"]
        logging.info(f"el usuario {userName} ha solicitado una buesqueda")

        brand = (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
        dsct = int(dsct)
        try:
         price = (context.args[2])
        except: price = None

        search_brand_dsct_html(brand,dsct,price, bot_token ,chat)

        document = open(config("HTML_PATH")+brand+".html", 'rb')
        await context.bot.send_document(chat, document)
        document.close()
        os.remove(config("HTML_PATH")+brand+".html")



    # async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #     query = update.callback_query
    #     await query.answer()
    
    #     if query.data == 1:
    #         print("opcion 1")
    #         async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #          await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text) 
    #         echo_handler= MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    #         application.add_handler(echo_handler)
    #         print("opcion 1")
    #     if query.data == 2:
    
    #             busqueda(str(codigo), config("CAPITAN_PIKE_TOKEN") ,config("ENTERPRISE_CHAT_TOKEN"))
                
    #     await query.edit_message_text(text=f"Seleccionaste opcion: {query.data}")
      


    async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No es un comando Valido recontra Gil...")

    #if __name__ == '__main__':
    #if __name__ == 'super_bot':
    application = ApplicationBuilder().token(TOKEN).build()
    
    print("asasdasd")
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)


    botinfo = CommandHandler('botinfo', getBotInfo)
    application.add_handler(botinfo)

    auto_te = CommandHandler('auto', auto_tele)
    application.add_handler(auto_te)

    commads = CommandHandler('comandos', Commands)
    application.add_handler(commads)

    custom_se = CommandHandler('b', custom_search)
    application.add_handler(custom_se)

    cat_lst = CommandHandler('cat', category_list)
    application.add_handler(cat_lst)

    brand_lst = CommandHandler('catlist', brand_list)
    application.add_handler(brand_lst)

    brand_add = CommandHandler('brand', add_brand)
    application.add_handler(brand_add)

    brand_del = CommandHandler('delete', brand_delete)
    application.add_handler(brand_del)

    manual_cat_search = CommandHandler('manual', auto_tele_dsct)
    application.add_handler(manual_cat_search)

    market = CommandHandler('market', custom_search_market)
    application.add_handler(market)

    codigo = CommandHandler('cod', sku)
    application.add_handler(codigo)

    send_html = CommandHandler('send', send_document)
    application.add_handler(send_html)

    send_prod = CommandHandler('product', send_product)
    application.add_handler(send_prod)


    brand_html = CommandHandler('marca', brand_to_html)
    application.add_handler(brand_html)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    send_html = CommandHandler('send', send_document)
    application.add_handler(send_html)

    #application.add_handler(CallbackQueryHandler(button))
    

   


    
    application.run_polling()


# chat = config("EXCELSIOR_CHAT_TOKEN")
# bot_token = config("TOKEN_PICARD")
# db1 = "excelsior1"
# db2 = "excelsior2"
# def test(bot_token ,chat, db1,db2):
#  super_bot( bot_token ,chat, db1,db2)