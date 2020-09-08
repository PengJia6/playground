# Title     : TODO
# Objective : TODO
# Created by: pengjia
# Created on: 2020/8/17

library(ggplot2)
library(ggsci)
fontstyle = "Arial"
fonttype = "Arial"
fontsize = 25
linesize = 1.5
plotpath <- "/home/pengjia/Desktop/FinalPlot/"
data <- read.csv(paste0("/mnt/project/MSIproject/Data/MSIsensor_pro/FinalTest/performance/CoverageRplot.csv"))
# data=subset(data,ml==3)
p <- ggplot(data = data, aes(
  x = ration,
  y = performance,
  color = factor(methods, levels = c("mantis", "MSIsensor", "mSINGS", "MSIsensor-pro(ALL)", "MSIsensor-pro(DMS)")),
  fill = factor(methods, levels = c("mantis", "MSIsensor", "mSINGS", "MSIsensor-pro(ALL)", "MSIsensor-pro(DMS)")),
  shape = tumorOnly,
  # x=factor(ration,levels = c("upstream","UTR5","splicing","exonic",
  #                          "intronic","ncRNA_splicing","ncRNA_exonic","ncRNA_intronic","UTR3","downstream","intergenic")),
  # color="black",
  # fill=factor(ml),
  # fill=factor(type,levels = c("Filter","DMS")),
  # color=factor(Func)
)
) +


  geom_point(size = 4) +
  scale_shape_manual(values = c(21, 24)) +
  geom_line(size = linesize) +
  facet_grid(~type, scales = "free") +
  # geom_bar(stat="identity",width = 0.8,alpha=0.8)+
  # geom_line(stat="density",size=linesize-0.5)+
  # geom_vline(xintercept = 0.0002)+

  ylab("AUC") +
  xlab("Sequencing depth (x)") +
  # # xlab("Gene region")+
  # labs(color="",fill="",shape="")+
  labs(colour = "", shape = "") +
  guides(fill = FALSE, color = FALSE, shape = FALSE) +


  # # geom_text(aes(,label=num),hjust=2,size=6)+
  # # scale_y_log10()+
  # scale_y_continuous(limits = c(0,0.02))+
  scale_x_continuous(, breaks = c(20, 40, 60, 80, 100), labels = c("20", "40", "60", "80", "100")) +
  scale_y_continuous(limits = c(0.4, 1.01), breaks = c(0.4, 0.6, 0.8, 1),) +
  # panel.spacing(unit)+
  # guides(color=FALSE,shape=FALSE)+


  theme_bw() +
  theme(
    axis.text.x = element_text(angle = 0, hjust = 0.5, vjust = -0, size = fontsize - 4, family = fonttype, colour = "black"),
    axis.text.y = element_text(angle = 0, hjust = 0.5, vjust = 0.5, size = fontsize - 2, family = fonttype, colour = "black"),
    axis.ticks.y.left = element_line(size = 0.5),
    axis.ticks.x = element_line(size = 0.5),

    plot.title = element_text(, size = fontsize + 3, hjust = 0.5, family = fonttype, colour = "black"),
    # panel.spacing = unit(2,"lines"),

    axis.title.x = element_text(face = "plain", size = fontsize - 2, vjust = -1, family = fonttype, colour = "black"),
    axis.title.y = element_text(face = "plain", size = fontsize, vjust = 3, family = fonttype, colour = "black"),
    # panel.background = element_rect(fill = "white", colour = "black"),
    panel.border = element_rect(fill = NA, color = "white", size = linesize),
    panel.grid.major.x = element_blank(),
    panel.grid.minor.x = element_blank(),
    panel.grid.major.y = element_blank(), #
    panel.grid.minor.y = element_blank(),
    # panel.grid.major.y=element_line(color="gray",size=1), #
    # panel.grid.minor.y=element_line(color="gray",size=1),
    # panel.margin = unit(2, "lines"),
    legend.background = element_blank(),
    legend.key = element_blank(),

    legend.key.height = unit(0.8, "cm"),
    legend.key.width = unit(1.8, "cm"),
    legend.key.size = unit(1.5, "cm"),
    # legend.position = "right",
    # legend.position = c(0.6,0.6),

    # legend.direction = "horizontal",
    legend.text = element_text(size = fontsize - 4, family = fonttype, colour = "black"),

    strip.text = element_text(size = fontsize, family = fonttype, colour = "white"),
    strip.background = element_rect(fill = "white", color = "white"),
    strip.placement = "inside",

    # axis.line =element_line()
    axis.line = element_line(color = "black", size = linesize),
    plot.margin = unit(c(0.5, 0.5, 0.5, 0.5), "cm")
  ) +
  scale_fill_nejm() +
  scale_color_nejm()
svg(paste0(plotpath, "", "coverage", ".svg"), width = 5.0, height = 4.5)
p
dev.off()
ggsave(paste0(plotpath, "", "coverage", ".png"), width = 5.0, height = 4.5, dpi = 500)


