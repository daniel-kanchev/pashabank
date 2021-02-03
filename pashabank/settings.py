BOT_NAME = 'pashabank'
SPIDER_MODULES = ['pashabank.spiders']
NEWSPIDER_MODULE = 'pashabank.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
ITEM_PIPELINES = {
   'pashabank.pipelines.DatabasePipeline': 300,
}
