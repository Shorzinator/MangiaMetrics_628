library(shiny)
library(shinydashboard)
library(leaflet)
library(dplyr)
library(ggplot2)
library(tidyr)
library(lubridate)
library(sf)
library(RColorBrewer)
library(readxl)
library(dplyr)
#install.packages("tigris")
library(tigris)
#install.packages("USAboundaries")
#library(USAboundaries)
library(leaflet.extras)
library(plotly)
options(tigris_use_cache = TRUE)

# Define UI
ui <- fluidPage(
  tabsetPanel(
    tabPanel("MAP",
             sidebarLayout(
               sidebarPanel(width = 2,
                            selectInput("colorBy", "Color Map By:", choices = c("OccupancyDensity", "Structures", "LivingSpaces", "Rent"))
               ),
               mainPanel(width = 10,
                         leafletOutput("map",height = "900px")
               )
             )
    ),
    tabPanel("Restaurant Explore",
             sidebarLayout
             (
               sidebarPanel(
                 sliderInput("ratingInput", "Minimum Rating:", min = 1, max = 5, value = 3, step = 0.5),
                 checkboxInput("deliveryInput", "Only Restaurants with Delivery", FALSE),
                 selectInput("nameInput", "Choose a Restaurant:", choices = NULL),
                 selectizeInput("zipCodeInput", "Choose a ZIP Code:", choices = NULL)
               ),
               mainPanel
               (
                 tabsetPanel(tabPanel("Restaurant Map", leafletOutput("map2")),
                             tabPanel("Restaurant Analysis", plotOutput("trendPlot"), plotOutput("ratingDistributionPlot")),
                             tabPanel("Demographic Analysis", plotOutput("populationOverview"), 
                                      fluidRow(column(6, plotlyOutput("healthInsurancePlot")),
                                               column(6, plotlyOutput("employmentStatusPlot")))))))),
    tabPanel("Suggestions",
             fluidRow(
               column(width = 6,
                      img(src = "Slide111.jpg", width = "100%")
               ),
               column(width = 6,
                      img(src = "slide121.jpg", width = "100%")
               )
             ),
             # Row for select input
             sidebarLayout
             (
               sidebarPanel(width = 2,
                            selectizeInput("zipCodeInput2", "Choose a ZIP Code:", choices = NULL)
               ),
               
               mainPanel(width = 10,
                         leafletOutput("map3",height = "700px")
               )) )
    
  )
)


server <- function(input, output,session) {
  # Page 1 Load data
  area_data <-read_excel("dp4.xlsx", sheet = 1) %>% 
    select("ZIP Code","Occupants per room - OHU - 1.51 or more", "GRAPI - 1 - 15.0 to 19.9 percent", "Rooms - THU - 2 rooms", "YSB - THU - Built 1939 or earlier" ) %>% 
    rename('ZIP'= "ZIP Code", 
           "OccupancyDensity" = "Occupants per room - OHU - 1.51 or more",
           "Structures" = "YSB - THU - Built 1939 or earlier", 
           "LivingSpaces" = "Rooms - THU - 2 rooms", 
           "Rent" = "GRAPI - 1 - 15.0 to 19.9 percent") %>% mutate(across(everything(), as.numeric)) %>% 
    mutate(ZIP= as.character(ZIP))
  
  #business_data <- read.csv("business_x_review.txt") %>% select(-"text") %>% rename( 'ZIP'= "ZIP.Code" )
  business_data2<- read.csv("BLL.csv") %>% rename('ZIP' = 'postal_code') %>% mutate(ZIP= as.character(ZIP))
  com_data<- read.csv("composite_metric.csv") %>% rename('ZIP' = 'ZIP_CODE',"success_score"="Composite_Metric") %>% mutate(ZIP= as.character(ZIP)) 
  
  zip_data <- zctas(state = "PA", cb = FALSE, class = "sf",year = 2010) %>% st_transform( crs = 4326) %>% rename('ZIP'= 'ZCTA5CE10') 
  combined_data1 <- left_join(area_data,com_data, by = 'ZIP') 
  combined_data0 <- left_join(business_data2,combined_data1 , by = 'ZIP') 
  combined_data <- right_join(zip_data, combined_data0, by = 'ZIP') %>% 
    mutate(OccupancyDensity = ifelse(is.na(OccupancyDensity), 0, OccupancyDensity),
           Structures = ifelse(is.na(Structures), 0, Structures),
           LivingSpaces = ifelse(is.na(LivingSpaces), 0, LivingSpaces),
           Rent = ifelse(is.na(Rent), 0, Rent),
           success_score = ifelse(is.na(success_score), 0, success_score))
  
  # Page 2 Load data
  restaurant_data <- read.csv("flattened_business.csv")
  review_data <- read.csv("flattened_review.csv")
  demographic_data <- read.csv("top_demographics.csv")
  
  
  # Update selectInput choices
  updateSelectInput(session, "nameInput", choices = c("All", unique(restaurant_data$name)))
  updateSelectizeInput(session, "zipCodeInput", choices = c("All",sort(unique(demographic_data$ZIP_CODE))), server = TRUE)
  updateSelectizeInput(session, "zipCodeInput2", choices = c("All",sort(unique(combined_data$ZIP))),selected = "All", server = TRUE)
  
  renderMap <- function(variable) {
    if(variable == "OccupancyDensity"){
      pal <- colorNumeric(palette = "viridis", domain = combined_data$OccupancyDensity)
      leaflet(data = combined_data) %>%
        addProviderTiles(providers$OpenStreetMap) %>%
        addPolygons(fillColor = ~pal(combined_data$OccupancyDensity),
                    fillOpacity = 0.05,
                    weight = 1,
                    color = "#444444",
                    popup = ~paste("ZIP Code:", ZIP, "<br>", "Occupants per room - OHU - 1.51 or more:", OccupancyDensity)) %>%
        addLegend(pal = pal, values = ~OccupancyDensity, title = "Occupancy Density")  %>%
        setView(lng = -75.25, lat =40.0 , zoom = 10) 
    }
    else if (variable == "Structures"){
      pal <- colorNumeric(palette = "viridis", domain = combined_data$Structures)
      leaflet(data = combined_data) %>%
        addProviderTiles(providers$OpenStreetMap) %>%
        addPolygons(fillColor = ~pal(Structures),
                    fillOpacity = 0.05,
                    weight = 1,
                    color = "#444444",
                    popup = ~paste("ZIP Code:", ZIP, "<br>", "YSB - THU - Built 1939 or earlier:", Structures)) %>%
        addLegend(pal = pal, values = ~Structures, title = "Structures") %>%  
        setView(lng = -75.25, lat =40.0 , zoom = 10) 
    }
    else if (variable == "LivingSpaces"){
      pal <- colorNumeric(palette = "viridis", domain = combined_data$LivingSpaces)
      leaflet(data = combined_data) %>%
        addProviderTiles(providers$OpenStreetMap) %>%
        addPolygons(fillColor = ~pal(LivingSpaces),
                    fillOpacity = 0.05,
                    weight = 1,
                    color = "#444444",
                    popup = ~paste("ZIP Code:", ZIP, "<br>", "Rooms - THU - 2 rooms:", LivingSpaces)) %>%
        addLegend(pal = pal, values = ~LivingSpaces, title = "LivingSpaces") %>%  
        setView(lng = -75.25, lat =40.0 , zoom = 10) 
    }
    else {
      pal <- colorNumeric(palette = "viridis", domain = combined_data$Rent)
      leaflet(data = combined_data) %>%
        addProviderTiles(providers$OpenStreetMap) %>%
        addPolygons(fillColor = ~pal(Rent),
                    fillOpacity = 0.05,
                    weight = 1,
                    color = "#444444",
                    popup = ~paste("ZIP Code:", ZIP, "<br>", "GRAPI - 1 - 15.0 to 19.9 percent:", OccupancyDensity)) %>%
        addLegend(pal = pal, values = ~Rent, title = "Rent") %>% 
        setView(lng = -75.25, lat =40.0 , zoom = 10) 
    }
  }
  
  output$map <- renderLeaflet({
    renderMap(input$colorBy)
  })
  
  #new output$map
  observeEvent(input$colorBy, {
    
    leafletProxy("map", data = combined_data) %>%
      clearMarkers() %>%  
      addMarkers(
        clusterOptions = markerClusterOptions(),
        lng = ~longitude,
        lat = ~latitude,
        popup = ~paste("Restaurant Name:", name,"<br>","star:",stars,"<br>","open or not:", is_open,"<br>","review count:", review_count) ) 
    
    
  })
  
  
  
  output$map3 <- renderLeaflet({
    selected_zip_code2 <- input$zipCodeInput2
    if (!is.null(selected_zip_code2) & selected_zip_code2 != "All") {
      filtered_data <- combined_data %>% filter(ZIP == selected_zip_code2)}
    else if (is.null(selected_zip_code2) & selected_zip_code2 == "All"){filtered_data <- combined_data}
    else{filtered_data <- combined_data}
    
    pal_all <- colorNumeric(palette = c("blue", "orange"), domain = combined_data$success_score)
    leaflet(data = filtered_data) %>%
      addProviderTiles(providers$OpenStreetMap) %>%
      addPolygons(fillColor = ~pal_all(success_score),
                  fillOpacity = 0.1,
                  weight = 1,
                  color = "#444444",
                  popup = ~paste("ZIP Code:", ZIP, "<br>", "Success Score:", sprintf("%.2f", success_score))) %>%
      addLegend(pal = pal_all, values = ~success_score, title = "success_score") %>% 
      setView(lng = -75.0, lat =40.05 , zoom = 10) 
  })
  
  

  
  observe({
    current_rating <- input$ratingInput
    filtered_restaurants <- restaurant_data %>%
      filter(stars >= current_rating) %>%
      `$`(name) %>%
      unique()
    updateSelectInput(session, "nameInput", choices = c("All", filtered_restaurants))
  })
  
  # Restaurant data processing for the map
  filteredData <- reactive({
    data <- restaurant_data %>%
      filter(stars >= input$ratingInput) %>%
      filter(if (input$deliveryInput) RestaurantsDelivery == "True" else TRUE)
    if (input$nameInput != "All") {
      data <- data %>% filter(name == input$nameInput)
    }
    return(data)
  })
  
  # Render map
  output$map2 <- renderLeaflet({
    leaflet(data = filteredData()) %>%
      addTiles() %>%
      addMarkers( ~longitude, ~latitude, popup = ~paste("Name:", name, "<br>", "Rating:", stars, "<br>", "ZIP Code:", `ZIP.Code`)) %>% 
      setView(lng = -75.25, lat =40.0 , zoom = 10) 
  })
  
  # Reactive expression for filtered review data
  filteredReviewData <- reactive({
    if (input$nameInput != "All") {
      selected_restaurant <- filteredData()
      if (nrow(selected_restaurant) > 0) {
        selected_business_id <- selected_restaurant$business_id[1]
        review_data %>% filter(business_id == selected_business_id)
      } else {
        data.frame() # empty data frame if no restaurant is selected
      }
    } else {
      review_data # all review data if "All" is selected
    }
  })
  
  # Render trend plot
  output$trendPlot <- renderPlot({
    review_subset <- filteredReviewData()
    if (nrow(review_subset) > 0) {
      review_subset$Date <- as.Date(review_subset$Date, format="%Y-%m-%d")
      review_subset$Year <- year(review_subset$Date)
      review_subset$Month <- month(review_subset$Date)
      
      monthly_avg <- review_subset %>%
        group_by(Year, Month) %>%
        summarize(AvgStars = mean(stars, na.rm = TRUE))
      
      ggplot(monthly_avg, aes(x = as.Date(paste(Year, Month, "01", sep="-")), y = AvgStars)) +
        geom_line() +
        labs(title = "Average Monthly Rating", x = "Date", y = "Average Stars") +
        theme_minimal()
    }
  })
  
  # Render rating distribution plot
  output$ratingDistributionPlot <- renderPlot({
    review_subset <- filteredReviewData()
    if (nrow(review_subset) > 0) {
      ggplot(review_subset, aes(x = stars)) +
        geom_histogram(binwidth = 0.5, fill = "blue", color = "black") +
        labs(title = "Rating Distribution", x = "Rating", y = "Count") +
        theme_minimal()
    }
  })
  
  plot_demographics_by_zip <- function(zip_code, data) {
    selected_data <- data %>% 
      filter(ZIP_CODE == zip_code) %>%
      select(-ZIP_CODE) %>% 
      pivot_longer(cols = everything(), names_to = "category", values_to = "value") %>%
      arrange(category) 
    
    colors <- colorRampPalette(RColorBrewer::brewer.pal(8, "Set3"))(length(unique(selected_data$category)))
    
    ggplot(selected_data, aes(x = category, y = value, fill = category)) +
      geom_bar(stat = "identity") +
      coord_flip() + 
      scale_fill_manual(values = colors) +
      theme_minimal() +
      theme(legend.position = "none") +
      labs(title = paste("Demographic Statistics for ZIP Code", zip_code),
           x = "Demographic Indicator",
           y = "Value")
  }
  output$populationOverview <- renderPlot({
    selected_zip_code <- input$zipCodeInput
    if (!is.null(selected_zip_code) && selected_zip_code != "All") {
      #selected_zip_code <- as.numeric(selected_zip_code)
      filtered_data <- demographic_data %>% filter(ZIP_CODE == selected_zip_code)
      
      if (nrow(filtered_data) > 0) {
        plot_demographics_by_zip(selected_zip_code,demographic_data)
      }
      }
      else if(selected_zip_code == "All"){
        data_sum <- demographic_data %>% 
          select(-ZIP_CODE) %>% 
          summarise_all(sum, na.rm = TRUE) %>% 
          pivot_longer(cols = everything(), names_to = "category", values_to = "value") %>%
          arrange(category) 
        
      
        colors2 <- colorRampPalette(RColorBrewer::brewer.pal(8, "Set3"))(length(unique(data_sum$category)))
        ggplot(data_sum, aes(x = category, y = value)) +
          geom_bar(stat = "identity") +
          coord_flip() +
          theme_minimal() +
          scale_fill_manual(values = colors2) + 
          labs(title = "Sum of Demographic Statistics Across All Regions",
               x = "Demographic Indicator",
               y = "Total Value")}
    })
  
  # Health Insurance Coverage Plot - Donut Chart
  output$healthInsurancePlot <- renderPlotly({
    selected_zip_code <- input$zipCodeInput
    if (!is.null(selected_zip_code) && selected_zip_code != "") {
      selected_zip_code <- as.numeric(selected_zip_code)
      filtered_data <- demographic_data %>% filter(ZIP_CODE == selected_zip_code)
      
      if (nrow(filtered_data) > 0) {
        insurance_population <- sum(filtered_data$`Health.Insurance.Coverage...Civilian.noninstitutionalized.population.19.to.64.years`, na.rm = TRUE)
        total_population <- max(demographic_data$`Health.Insurance.Coverage...Civilian.noninstitutionalized.population.19.to.64.years`, na.rm = TRUE)
        
        data <- data.frame(
          Category = c("Covered", "Not Covered"),
          Values = c(insurance_population, total_population - insurance_population)
        )
        
        p <- plot_ly(data, labels = ~Category, values = ~Values, type = 'pie', hole = 0.6) %>%
          layout(title = paste("Health Insurance Coverage in ZIP Code", selected_zip_code),
                 showlegend = TRUE)
        p
      } else {
        plotly_empty()
      }
    }
  })
  
  # Employment Status Plot - Donut Chart
  output$employmentStatusPlot <- renderPlotly({
    selected_zip_code <- input$zipCodeInput
    if (!is.null(selected_zip_code) && selected_zip_code != "") {
      selected_zip_code <- as.numeric(selected_zip_code)
      filtered_data <- demographic_data %>% filter(ZIP_CODE == selected_zip_code)
      
      if (nrow(filtered_data) > 0) {
        employment_population <- sum(filtered_data$`Employment.Status...Population.16.years.and.over`, na.rm = TRUE)
        total_population <- max(demographic_data$`Employment.Status...Population.16.years.and.over`, na.rm = TRUE)
        
        data <- data.frame(
          Category = c("Employed", "Unemployed"),
          Values = c(employment_population, total_population - employment_population)
        )
        
        p <- plot_ly(data, labels = ~Category, values = ~Values, type = 'pie', hole = 0.6) %>%
          layout(title = paste("Employment Status in ZIP Code", selected_zip_code),
                 showlegend = TRUE)
        
        p
      } else {
        plotly_empty()
      }
    }
  })
  
  
}

shinyApp(ui = ui, server = server)
