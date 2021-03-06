#packages
library(ggplot2)
library(dplyr)
library(reshape2)
library(data.table)
library(tidyr)
library(tidyverse)
library(readxl)
library(RColorBrewer)
library(plotly)

#read data
raw <- read_excel('C:\\Side Projects\\houses\\house_data.xlsx', sheet = 'Sheet1', col_names = TRUE)

#user created function
getmode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

#checks
names(raw)
str(raw)
summary(raw)

#drop index
raw <- raw[,2:ncol(raw)]

raw$city <- ifelse(grepl("Waterford", raw$address), 'Wat', 'Dub')
raw$floor_value <- as.numeric(gsub("m.|a.","", raw$floor_area))
raw$floor_metric <- gsub(".*(?=[am])", "", raw$floor_area, perl = TRUE)


#price stats
raw %>%
  group_by(city, prop_type) %>%
  summarise(count = n(),
            avg = round(mean(price, na.rm = TRUE), 2),
            min = min(price, na.rm = TRUE),
            q1 = round(quantile(price, 0.25, na.rm = TRUE), 2),
            med = round(median(price, na.rm = TRUE), 2),
            q3 = round(quantile(price, 0.75, na.rm = TRUE), 2),
            max = max(price, na.rm = TRUE),
            med_beds = median(beds, na.rm = TRUE),
            .groups = 'drop'
  ) %>%
  filter(!is.na(prop_type)) %>%
  melt(id.vars = c("city", "prop_type", "count"),
       variable.name = "stat",
       value.name = "value") %>%
  ggplot(aes(x = city, y = value, fill = city)) +
           geom_bar(stat ='identity') +
  facet_grid(stat ~ prop_type, scales = 'free') +
  ggtitle('Dublin V Waterford Price Stats by Property Type') +
  scale_y_continuous(labels = scales::comma) +
  scale_fill_manual(values = c('#C2D8FF', '#00276C')) +
  theme(plot.title = element_text(hjust = 0.5, face = 'bold'),
        axis.title.x = element_text(face = 'bold'),
        axis.title.y = element_text(face = 'bold'),
        panel.background = element_rect(fill = 'white', color = '#C2D8FF'),
        panel.grid = element_line(color = '#C2D8FF'),
        strip.background = element_rect(colour="#C2D8FF", fill="darkblue"),
        strip.text = element_text(face = 'bold', color = 'white')
        
  )

#price boxplots
raw %>%
  filter(!is.na(price) & !is.na(prop_type) & price <1000000)  %>%
  ggplot(aes(x = city, y = price, fill = city)) +
  geom_boxplot(outlier.colour="darkblue", outlier.shape=8,
               outlier.size=1,  color = '#FF02E4') +
  facet_wrap(~ prop_type, scales ='free') +
  ggtitle('Dublin V Waterford Property Prices by Property Type') +
  scale_y_continuous(labels = scales::comma) +
  scale_fill_manual(values = c('#C2D8FF', '#00276C')) +
  theme(plot.title = element_text(hjust = 0.5, face = 'bold'),
        axis.title.x = element_text(face = 'bold'),
        axis.title.y = element_text(face = 'bold'),
        panel.background = element_rect(fill = 'white', color = '#C2D8FF'),
        panel.grid = element_line(color = '#C2D8FF'),
        strip.background = element_rect(colour="#C2D8FF", fill="darkblue"),
        strip.text = element_text(face = 'bold', color = 'white')
        
  )
  
#price hists
raw %>%
  filter(!is.na(price) & !is.na(prop_type) & price <1000000)  %>%
  ggplot(aes(x = price, fill = city)) +
  geom_histogram(alpha=0.6, position="identity") +
  facet_wrap(~ prop_type, scales = 'free') +
  ggtitle('Dublin V Waterford Property Prices by Property Type') +
  scale_fill_manual(values = c('#C2D8FF', '#00276C')) +
  theme(plot.title = element_text(hjust = 0.5, face = 'bold'),
        axis.title.x = element_text(face = 'bold'),
        axis.title.y = element_text(face = 'bold'),
        panel.background = element_rect(fill = 'white', color = '#C2D8FF'),
        panel.grid = element_line(color = '#C2D8FF'),
        strip.background = element_rect(colour="#C2D8FF", fill="darkblue"),
        strip.text = element_text(face = 'bold', color = 'white')
  )

#floor space boxplots m2
raw %>%
  filter(!is.na(floor_value) & !is.na(prop_type) & floor_metric == 'm2' & floor_value <1000)  %>%
  ggplot(aes(x = city, y = floor_value, fill = city)) +
  geom_boxplot(outlier.colour="darkblue", outlier.shape=8,
               outlier.size=1, color = '#FF02E4') +
  facet_wrap(~ prop_type, scales ='free') +
  ggtitle('Dublin V Waterford Property Floor Area (m2) by Property Type') +
  scale_y_continuous(labels = scales::comma) +
  scale_fill_manual(values = c('#C2D8FF', '#00276C')) +
  theme(plot.title = element_text(hjust = 0.5, face = 'bold'),
        axis.title.x = element_text(face = 'bold'),
        axis.title.y = element_text(face = 'bold'),
        panel.background = element_rect(fill = 'white', color = '#C2D8FF'),
        panel.grid = element_line(color = '#C2D8FF'),
        strip.background = element_rect(colour="#C2D8FF", fill="darkblue"),
        strip.text = element_text(face = 'bold', color = 'white')
        
  )

#floor arce
raw %>%
  filter(!is.na(floor_value) & !is.na(prop_type) & floor_metric == 'ac' & floor_value <10)  %>%
  ggplot(aes(x = city, y = floor_value, fill = city)) +
  geom_boxplot(outlier.colour="darkblue", outlier.shape=8,
               outlier.size=1,  color = '#FF02E4') +
  facet_wrap(~ prop_type, scales ='free') +
  ggtitle('Dublin V Waterford Property Floor Area (ac) by Property Type') +
  scale_y_continuous(labels = scales::comma) +
  scale_fill_manual(values = c('#C2D8FF', '#00276C')) +
  theme(plot.title = element_text(hjust = 0.5, face = 'bold'),
        axis.title.x = element_text(face = 'bold'),
        axis.title.y = element_text(face = 'bold'),
        panel.background = element_rect(fill = 'white', color = '#C2D8FF'),
        panel.grid = element_line(color = '#C2D8FF'),
        strip.background = element_rect(colour="#C2D8FF", fill="darkblue"),
        strip.text = element_text(face = 'bold', color = 'white')
        
  )

#3d scatter of floor, beds and price by county
raw %>%
  filter(!is.na(floor_value) 
         & !is.na(prop_type) 
         & floor_metric == 'm2'
         & floor_value <1000
         & price <1000000
         ) %>%
plot_ly(x = ~floor_value, y = ~price, z = ~beds, color = ~city, colors =  c('#C2D8FF', '#00276C')) %>%
   layout(title = 'Waterford/Dublin Price (<1m), floor m2 (<1000m2) and Beds ')

