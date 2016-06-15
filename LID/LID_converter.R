library(jsonlite)
library(plyr)

path = "~/azcir/LID/jsonResults"
file.names <- dir(path, pattern =".json")

parse_line <- function(data){
    #Column
    query_document_id <- data$query_document_id
    alignment_results <- data$alignment_results

    if(length(alignment_results) == 0){
        print(paste("No alignment_results for", query_document_id))
        df <- data.frame(query_document_id=query_document_id)
        return(df)
    }else{
        #print(paste("AR:",nrow(alignment_results)))
        acum <- data.frame()
        for (i in 1:nrow(alignment_results)){
            #lucene score (no)
            #document_id (yes)
            row <- alignment_results[i,]
            doc_id <- row$document_id
            #Then for each alignment get
            #left, left_end, left_start, right, right_end, right_start, score
            alignment <- as.data.frame(row$alignments)
            right <- unlist(lapply(alignment$right, paste, collapse=" "))
            left <- unlist(lapply(alignment$left, paste, collapse=" "))

            df <- data.frame(left, right)
            df$left_end <- alignment$left_end
            df$left_start <- alignment$left_start
            df$right_end <- alignment$right_end
            df$right_start <- alignment$right_start
            df$score <- alignment$score
            df$doc_id <- doc_id
            df$query_document_id <- query_document_id
            #print(paste("INNER:",nrow(df)))
            acum <- rbind(acum, df)
        }
        return(acum)
    }
}

for(i in 1:length(file.names)){
    library(tools)
    fn_split <- file_path_sans_ext(basename(file.names[i]))
    output_file <- paste(fn_split, ".csv", sep = "")
    conn <- file(file.names[i], open="r")
    lines <- readLines(conn)
    data <- lapply(lines, fromJSON)
    df_line <- lapply(data, parse_line)
    df <- rbind.fill(df_line)
    write.csv(df, output_file, fileEncoding="UTF-8")
}
